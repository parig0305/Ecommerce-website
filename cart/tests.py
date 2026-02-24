from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from products.models import Product, ProductVariant
from cart.models import Cart, CartItem
from orders.models import Order


class CartCheckoutTests(TestCase):
	def setUp(self):
		self.client = Client()
		User = get_user_model()
		self.user = User.objects.create_user(username='testuser', password='testpass', email='t@example.com')

		# Create product and variant
		self.product = Product.objects.create(name='Test Product', description='desc', price='50.00', category='test')
		self.variant = ProductVariant.objects.create(product=self.product, size='M', color='Red', stock=5)

	def test_add_to_cart_and_checkout_cod(self):
		# login
		self.client.login(username='testuser', password='testpass')

		# add to cart
		resp = self.client.post('/cart/add/', {'product_id': self.product.id, 'variant_id': self.variant.id, 'quantity': 2})
		self.assertEqual(resp.status_code, 302)  # redirect to cart

		cart = Cart.objects.filter(user=self.user).first()
		self.assertIsNotNone(cart)
		self.assertEqual(cart.get_item_count(), 2)

		# checkout (create order)
		resp = self.client.post('/orders/create/', {'address': '123', 'phone': '9999', 'payment_method': 'cod'}, follow=True)
		self.assertEqual(resp.status_code, 200)

		order = Order.objects.filter(user=self.user).order_by('-created_at').first()
		self.assertIsNotNone(order)
		self.assertEqual(float(order.total_price), float(100.00))

	def test_out_of_stock_prevention(self):
		self.client.login(username='testuser', password='testpass')

		# try to add more than stock
		resp = self.client.post('/cart/add/', {'product_id': self.product.id, 'variant_id': self.variant.id, 'quantity': 10}, follow=True)
		# should redirect to product detail (or show error); cart should not have the item
		cart = Cart.objects.filter(user=self.user).first()
		if cart:
			self.assertNotEqual(cart.get_item_count(), 10)

