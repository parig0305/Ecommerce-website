from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.core.mail import send_mail
import razorpay
import stripe
from orders.models import Order
from cart.models import Cart
from django.urls import reverse
import qrcode
import base64
from io import BytesIO
import logging


# Initialize Razorpay client only when keys are provided via environment
razorpay_client = None
try:
    if getattr(settings, 'RAZORPAY_KEY_ID', None) and getattr(settings, 'RAZORPAY_KEY_SECRET', None):
        # Avoid using placeholder values
        if not str(settings.RAZORPAY_KEY_ID).startswith('your') and not str(settings.RAZORPAY_KEY_SECRET).startswith('your'):
            razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        else:
            logging.warning('Razorpay keys look like placeholders; client not initialized.')
    else:
        logging.info('Razorpay keys not found in settings; client not initialized.')
except Exception as e:
    logging.exception('Failed to initialize Razorpay client: %s', e)

# Initialize Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY if hasattr(settings, 'STRIPE_SECRET_KEY') else None


@login_required
def checkout(request, order_id=None):
    """Checkout page with payment options"""
    # Get user's cart
    cart = Cart.objects.filter(user=request.user).first()
    
    if not cart or not cart.items.exists():
        messages.error(request, "Your cart is empty")
        return redirect('cart')

    # Get order if provided
    if order_id:
        order = get_object_or_404(Order, id=order_id, user=request.user)
    else:
        # Check if there's a pending order
        existing_order = Order.objects.filter(user=request.user, payment_status='pending').first()
        if existing_order:
            order = existing_order
        else:
            # Create a new order (temporary, will update after payment)
            order = None

    context = {
        'order': order,
        'cart': cart,
        'cart_items': cart.items.all(),
        'total': cart.get_total(),
        'total_items': cart.get_item_count(),
        'razorpay_key': settings.RAZORPAY_KEY_ID if razorpay_client else None,
    }
    return render(request, 'checkout.html', context)


@login_required
def initiate_payment(request, order_id):
    """Initiate Razorpay payment"""
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if not razorpay_client:
        messages.error(request, "Razorpay payment gateway not configured")
        return redirect('checkout')

    # Create Razorpay order
    razorpay_order = razorpay_client.order.create({
        'amount': int(order.total_price * 100),  # Convert to paise
        'currency': 'INR',
        'receipt': f'receipt_{order.id}',
        'payment_capture': 1
    })

    # Save razorpay order ID
    order.razorpay_order_id = razorpay_order['id']
    order.payment_method = 'razorpay'
    order.save()

    context = {
        'order': order,
        'razorpay_key': settings.RAZORPAY_KEY_ID,
        'razorpay_order': razorpay_order,
    }
    return render(request, 'razorpay_payment.html', context)


@login_required
def razorpay_qr(request, order_id):
    """Create a Razorpay payment link and return a QR code for the link"""
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if not razorpay_client:
        messages.error(request, "Razorpay payment gateway not configured")
        return redirect('checkout')

    # Create a payment link
    try:
        link = razorpay_client.payment_link.create({
            'amount': int(order.total_price * 100),
            'currency': 'INR',
            'accept_partial': False,
            'description': f'Payment for {order.order_id}',
            'customer': {
                'name': order.user.get_full_name() or order.user.username,
                'email': order.user.email,
            },
            'notify': {'sms': False, 'email': False},
            'callback_url': request.build_absolute_uri(reverse('razorpay_callback')),
        })

        pay_url = link.get('short_url') or link.get('long_url')

        # Generate QR code image as base64
        qr = qrcode.QRCode(box_size=8, border=2)
        qr.add_data(pay_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buf = BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        img_b64 = base64.b64encode(buf.read()).decode('ascii')

        context = {
            'order': order,
            'pay_url': pay_url,
            'qr_b64': img_b64,
        }
        return render(request, 'razorpay_qr.html', context)

    except Exception as e:
        messages.error(request, f"Failed to create payment link: {str(e)}")
        return redirect('checkout')


@csrf_exempt
def razorpay_callback(request):
    """Handle Razorpay payment callback"""
    if request.method == 'POST':
        try:
            payment_id = request.POST.get('razorpay_payment_id')
            order_id = request.POST.get('razorpay_order_id')
            signature = request.POST.get('razorpay_signature')

            # Verify signature
            if razorpay_client:
                razorpay_client.utility.verify_payment_signature({
                    'razorpay_order_id': order_id,
                    'razorpay_payment_id': payment_id,
                    'razorpay_signature': signature
                })

            # Update order
            order = Order.objects.get(razorpay_order_id=order_id)
            order.payment_id = payment_id
            order.payment_status = 'completed'
            order.status = 'processing'
            order.save()

            # Clear cart
            user_cart = Cart.objects.filter(user=order.user).first()
            if user_cart:
                user_cart.items.all().delete()

            # Send confirmation email
            try:
                send_mail(
                    f'Payment Successful - Order {order.order_id}',
                    f'Your payment of ₹{order.total_price} has been successful!\n\n'
                    f'Order ID: {order.order_id}\n'
                    f'Payment ID: {payment_id}\n\n'
                    f'Thank you for shopping with us!',
                    settings.DEFAULT_FROM_EMAIL,
                    [order.user.email],
                    fail_silently=True,
                )
            except:
                pass

            messages.success(request, "Payment successful! Order placed successfully.")
            return redirect('order_detail', order_id=order.order_id)

        except Exception as e:
            messages.error(request, f"Payment verification failed: {str(e)}")
            return redirect('order_history')

    return redirect('home')


@login_required
def stripe_payment(request, order_id):
    """Initiate Stripe payment"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if not stripe.api_key:
        messages.error(request, "Stripe payment gateway not configured")
        return redirect('checkout')

    try:
        # Create Stripe checkout session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'inr',
                    'product_data': {
                            'name': f'Order {order.order_id}',
                            'description': f'Purchase from Pari kart',
                        },
                    'unit_amount': int(order.total_price * 100),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri(f'/payments/stripe/success/?session_id={{CHECKOUT_SESSION_ID}}&order_id={order.id}'),
            cancel_url=request.build_absolute_uri(f'/payments/stripe/cancel/'),
            customer_email=request.user.email,
        )
        
        order.payment_method = 'stripe'
        order.save()
        
        return redirect(session.url, code=303)
        
    except Exception as e:
        messages.error(request, f"Payment error: {str(e)}")
        return redirect('checkout')


@login_required
def stripe_success(request):
    """Handle Stripe payment success"""
    session_id = request.GET.get('session_id')
    order_id = request.GET.get('order_id')
    
    if not stripe.api_key:
        messages.error(request, "Stripe payment gateway not configured")
        return redirect('order_history')
    
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        
        if session.payment_status == 'paid':
            order = Order.objects.get(id=order_id, user=request.user)
            order.payment_id = session.payment_intent
            order.payment_status = 'completed'
            order.status = 'processing'
            order.save()
            
            # Clear cart
            user_cart = Cart.objects.filter(user=request.user).first()
            if user_cart:
                user_cart.items.all().delete()
            
            # Send confirmation email
            try:
                send_mail(
                    f'Payment Successful - Order {order.order_id}',
                    f'Your payment of ₹{order.total_price} has been successful!\n\n'
                    f'Order ID: {order.order_id}\n'
                    f'Thank you for shopping with us!',
                    settings.DEFAULT_FROM_EMAIL,
                    [request.user.email],
                    fail_silently=True,
                )
            except:
                pass
            
            messages.success(request, "Payment successful! Order placed successfully.")
            return redirect('order_detail', order_id=order.order_id)
    
    except Exception as e:
        messages.error(request, f"Payment verification failed: {str(e)}")
    
    return redirect('order_history')


@login_required
def stripe_cancel(request):
    """Handle Stripe payment cancel"""
    messages.warning(request, "Payment was cancelled. Please try again.")
    return redirect('checkout')


@login_required
def payment_success(request):
    """Payment success page"""
    return render(request, 'payment_success.html')


@login_required
def payment_failed(request):
    """Payment failed page"""
    return render(request, 'payment_failed.html')
