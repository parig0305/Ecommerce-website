import os
import sys
from pathlib import Path
import django

# Ensure project root is on sys.path so Django settings module can be imported
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from products.models import Product, ProductVariant

User = get_user_model()

c = Client()

# Create or get test user
username = 'testuser'
email = 'testuser@example.com'
password = 'testpass123'
user, created = User.objects.get_or_create(username=username, defaults={'email': email})
if created:
    user.set_password(password)
    user.save()

# Create a product and variant if not exists
product, _ = Product.objects.get_or_create(name='Test Product', defaults={
    'description': 'A test product',
    'price': '99.99',
    'category': 'test',
})

variant, _ = ProductVariant.objects.get_or_create(product=product, size='M', color='Red', defaults={'stock': 10})

# Login
logged_in = c.login(username=username, password=password)
if not logged_in:
    # If login failed, set session manually by force_login
    c.force_login(user)

print('User logged in')

# Add to cart
resp = c.post('/cart/add/', {'product_id': product.id, 'variant_id': variant.id, 'quantity': 2}, follow=True)
print('Add to cart status code:', resp.status_code)

# View cart
resp = c.get('/cart/')
print('Cart page status code:', resp.status_code)
if b'Test Product' in resp.content:
    print('Product is present in cart page HTML')

# Proceed to create order (checkout) - POST to orders/create/
resp = c.post('/orders/create/', {'address': '123 Test St', 'phone': '9999999999', 'payment_method': 'cod'}, follow=True)
print('Create order status code:', resp.status_code)

if resp.redirect_chain:
    print('Redirect chain:', resp.redirect_chain)

# Look for order confirmation in messages or order detail
if resp.status_code == 200 and b'Order placed successfully' in resp.content:
    print('Order placed successfully (message detected)')
else:
    print('Order response size:', len(resp.content))

# Print last order for the user
from orders.models import Order
last_order = Order.objects.filter(user=user).order_by('-created_at').first()
if last_order:
    print('Last order id:', last_order.order_id)
    print('Order total:', last_order.total_price)
else:
    print('No orders found for user')
