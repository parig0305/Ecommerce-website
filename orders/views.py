from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from .models import Order, OrderItem
from cart.models import Cart
from products.models import ProductVariant
import random
import string
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from io import BytesIO
from datetime import datetime


def generate_order_id():
    """Generate unique order ID"""
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    return f"ORD-{random_str}"


@login_required
def order_history(request):
    """View order history"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'order_history.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    """View order detail"""
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    return render(request, 'order_detail.html', {'order': order})


@login_required
def create_order(request):
    """Create order from cart"""
    if request.method == 'POST':
        cart = Cart.objects.filter(user=request.user).first()

        if not cart or not cart.items.exists():
            messages.error(request, "Your cart is empty")
            return redirect('cart')

        # Get form data
        shipping_address = request.POST.get('address', '')
        phone = request.POST.get('phone', '')
        payment_method = request.POST.get('payment_method', 'cod')

        if not shipping_address:
            messages.error(request, "Please provide shipping address")
            return redirect('checkout')

        # Create order
        order = Order.objects.create(
            user=request.user,
            order_id=generate_order_id(),
            total_price=cart.get_total(),
            shipping_address=shipping_address,
            phone=phone,
            status='pending',
            payment_method=payment_method
        )

        # Create order items
        for cart_item in cart.items.all():
            price = cart_item.variant.product.price if cart_item.variant else cart_item.product.price

            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                variant=cart_item.variant,
                quantity=cart_item.quantity,
                price=price
            )

            # Update stock
            if cart_item.variant:
                cart_item.variant.stock -= cart_item.quantity
                cart_item.variant.save()

        # Clear cart
        cart.items.all().delete()

        # Handle payment based on method
        if payment_method == 'cod':
            order.payment_status = 'pending'
            order.save()
            
            # Send confirmation email
            try:
                send_mail(
                    f'Order Confirmation - {order.order_id}',
                    f'Thank you for your order! Your order ID is {order.order_id}.\n\nTotal: ₹{order.total_price}\n\nPayment Method: Cash on Delivery',
                    settings.DEFAULT_FROM_EMAIL,
                    [request.user.email],
                    fail_silently=True,
                )
            except:
                pass

            messages.success(request, f"Order placed successfully! Order ID: {order.order_id}")
            return redirect('order_detail', order_id=order.order_id)
        
        elif payment_method == 'razorpay':
            # Redirect to payment page (use numeric PK for payment URL)
            return redirect('initiate_payment', order_id=order.id)
        
        elif payment_method == 'stripe':
            # Redirect to stripe payment (use numeric PK)
            return redirect('stripe_payment', order_id=order.id)

    return redirect('cart')


@login_required
def cancel_order(request, order_id):
    """Cancel order"""
    order = get_object_or_404(Order, order_id=order_id, user=request.user)

    if order.status in ['pending', 'processing']:
        # Restore stock
        for item in order.items.all():
            if item.variant:
                item.variant.stock += item.quantity
                item.variant.save()

        order.status = 'cancelled'
        order.save()
        messages.success(request, "Order cancelled successfully")
    else:
        messages.error(request, "Cannot cancel this order")

    return redirect('order_history')


@login_required
def download_invoice(request, order_id):
    """Generate and download PDF invoice"""
    order = get_object_or_404(Order, order_id=order_id, user=request.user)

    # Create PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)

    # Get styles
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    heading_style = styles['Heading2']
    normal_style = styles['Normal']

    # Create custom styles
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.gray
    )

    # Build content
    content = []

    # Company Header
    content.append(Paragraph("Pari kart - Invoice", title_style))
    content.append(Paragraph("123 E-Commerce Street, Online City, India", subtitle_style))
    content.append(Paragraph("Phone: +91 9876543210 | Email: support@parikart.com", subtitle_style))
    content.append(Spacer(1, 20))

    # Invoice Details
    content.append(Paragraph(f"<b>Invoice Number:</b> {order.order_id}", normal_style))
    content.append(Paragraph(f"<b>Date:</b> {order.created_at.strftime('%d-%m-%Y %H:%M')}", normal_style))
    content.append(Paragraph(f"<b>Status:</b> {order.get_status_display()}", normal_style))
    content.append(Spacer(1, 20))

    # Customer Details
    content.append(Paragraph("<b>Bill To:</b>", heading_style))
    content.append(Paragraph(f"{request.user.get_full_name() or request.user.username}", normal_style))
    content.append(Paragraph(f"Email: {request.user.email}", normal_style))
    content.append(Paragraph(f"Phone: {order.phone}", normal_style))
    content.append(Paragraph(f"Address: {order.shipping_address}", normal_style))
    content.append(Spacer(1, 20))

    # Items Table
    table_data = [['Item', 'Variant', 'Qty', 'Price', 'Total']]

    for item in order.items.all():
        variant_info = f"{item.variant.size} / {item.variant.color}" if item.variant else "-"
        table_data.append([
            item.product.name,
            variant_info,
            str(item.quantity),
            f"₹{item.price}",
            f"₹{item.get_total()}"
        ])

    # Add totals
    table_data.append(['', '', '', 'Subtotal:', f"₹{order.total_price}"])
    table_data.append(['', '', '', 'Shipping:', 'Free'])
    table_data.append(['', '', '', 'Total:', f"₹{order.total_price}"])

    # Create table
    table = Table(table_data, colWidths=[2*inch, 1.5*inch, 0.5*inch, 1*inch, 1*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -3), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -3), colors.black),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    content.append(table)
    content.append(Spacer(1, 30))

    # Payment Details
    content.append(Paragraph("<b>Payment Details:</b>", heading_style))
    content.append(Paragraph(f"Payment ID: {order.payment_id or 'Pending'}", normal_style))
    content.append(Paragraph(f"Payment Status: {order.payment_status}", normal_style))
    content.append(Paragraph(f"Payment Method: {order.payment_method.title() if order.payment_method else 'COD'}", normal_style))
    content.append(Spacer(1, 20))

    # Footer
    content.append(Paragraph("<b>Terms & Conditions:</b>", heading_style))
    content.append(Paragraph("1. This is a computer-generated invoice.", normal_style))
    content.append(Paragraph("2. Goods once sold cannot be returned.", normal_style))
    content.append(Paragraph("3. Please contact support for any queries.", normal_style))
    content.append(Spacer(1, 30))
    content.append(Paragraph("Thank you for shopping with us!", normal_style))

    # Build PDF
    doc.build(content)

    # Get PDF content
    buffer.seek(0)
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{order.order_id}.pdf"'

    return response
