from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from .models import Product, ProductVariant
from cart.models import Cart, CartItem, Wishlist
from cart.views import get_cart


def home(request):
    """Home page with product listing and search/filter"""
    # Get search query
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')
    sort_by = request.GET.get('sort', '-created_at')
    
    # Base queryset
    products = Product.objects.all()
    
    # Apply search
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query) |
            Q(category__icontains=search_query)
        )
    
    # Apply category filter
    if category_filter:
        products = products.filter(category__iexact=category_filter)
    
    # Apply sorting
    if sort_by:
        products = products.order_by(sort_by)
    
    # Get categories for filter dropdown
    categories = Product.objects.values_list('category', flat=True).distinct()
    
    # Get cart count
    try:
        cart = get_cart(request)
        cart_count = cart.get_item_count()
    except:
        cart_count = 0
    
    context = {
        'products': products,
        'categories': categories,
        'search_query': search_query,
        'category_filter': category_filter,
        'sort_by': sort_by,
        'cart_count': cart_count,
    }
    return render(request, 'home.html', context)


def products(request):
    """Products listing page with filters"""
    return home(request)


def product_detail(request, id):
    """Product detail page"""
    product = get_object_or_404(Product, id=id)
    variants = product.variants.all()
    
    # Get unique sizes and colors
    sizes = variants.values_list('size', flat=True).distinct()
    colors = variants.values_list('color', flat=True).distinct()
    
    # Get related products (same category)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    
    # Check if product is in wishlist
    in_wishlist = False
    if request.user.is_authenticated:
        in_wishlist = Wishlist.objects.filter(user=request.user, product=product).exists()
    
    # Get cart count
    try:
        cart = get_cart(request)
        cart_count = cart.get_item_count()
    except:
        cart_count = 0
    
    context = {
        'product': product,
        'variants': variants,
        'sizes': sizes,
        'colors': colors,
        'related_products': related_products,
        'in_wishlist': in_wishlist,
        'cart_count': cart_count,
    }
    return render(request, 'product_detail.html', context)


def category_products(request, category):
    """Products by category"""
    products = Product.objects.filter(category__iexact=category)
    context = {
        'products': products,
        'category': category,
    }
    return render(request, 'home.html', context)
