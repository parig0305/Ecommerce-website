from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Cart, CartItem, Wishlist
from products.models import Product, ProductVariant


def get_cart(request):
    """Get or create cart based on user or session"""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart


def cart_detail(request):
    """View cart contents"""
    cart = get_cart(request)
    items = cart.items.all()

    # Calculate total items
    total_items = sum(item.quantity for item in items)

    context = {
        'cart': cart,
        'cart_items': items,
        'total': cart.get_total(),
        'total_items': total_items,
    }
    return render(request, 'cart.html', context)


def add_to_cart(request):
    """Add item to cart"""
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        variant_id = request.POST.get('variant_id')
        quantity = int(request.POST.get('quantity', 1))

        product = get_object_or_404(Product, id=product_id)
        variant = None
        if variant_id:
            variant = get_object_or_404(ProductVariant, id=variant_id)
            # Check stock
            if variant.stock < quantity:
                messages.error(request, f"Only {variant.stock} items available in stock")
                return redirect('product_detail', id=product_id)

        cart = get_cart(request)

        # Check if item already in cart
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            variant=variant,
            defaults={'quantity': quantity}
        )

        if not created:
            cart_item.quantity += quantity
            # Check stock
            if variant and cart_item.quantity > variant.stock:
                messages.error(request, f"Only {variant.stock} items available in stock")
                return redirect('product_detail', id=product_id)
            cart_item.save()

        messages.success(request, f"{product.name} added to cart!")
        return redirect('cart')

    return redirect('home')


def update_cart_item(request, item_id, action):
    """Update cart item quantity - increase or decrease"""
    cart_item = get_object_or_404(CartItem, id=item_id)

    if action == 'increase':
        # Check stock
        if cart_item.variant and cart_item.quantity >= cart_item.variant.stock:
            messages.error(request, f"Only {cart_item.variant.stock} items available")
            return redirect('cart')
        cart_item.quantity += 1
        cart_item.save()
    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

    return redirect('cart')


def remove_from_cart(request, item_id):
    """Remove item from cart"""
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    messages.success(request, "Item removed from cart")
    return redirect('cart')


def clear_cart(request):
    """Clear all items from cart"""
    cart = get_cart(request)
    cart.items.all().delete()
    messages.success(request, "Cart cleared")
    return redirect('cart')


# Wishlist Views
@login_required
def wishlist(request):
    """View wishlist"""
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})


@login_required
def add_to_wishlist(request, product_id):
    """Add product to wishlist"""
    product = get_object_or_404(Product, id=product_id)

    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )

    if created:
        messages.success(request, f"{product.name} added to wishlist!")
    else:
        messages.info(request, f"{product.name} is already in your wishlist!")

    # Redirect back to the page user came from
    return redirect(request.META.get('HTTP_REFERER', 'product_detail', id=product_id))


@login_required
def remove_from_wishlist(request, item_id):
    """Remove product from wishlist"""
    wishlist_item = get_object_or_404(Wishlist, id=item_id, user=request.user)
    product_name = wishlist_item.product.name
    wishlist_item.delete()
    messages.success(request, f"{product_name} removed from wishlist")
    return redirect('wishlist')


def get_cart_count(request):
    """AJAX - Get cart item count"""
    cart = get_cart(request)
    return JsonResponse({'count': cart.get_item_count()})
