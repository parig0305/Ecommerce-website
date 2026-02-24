from django.db import models
from django.contrib.auth.models import User
from products.models import Product, ProductVariant
from django.utils import timezone
import random
import string


def generate_order_id():
    """Generate unique order ID"""
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    return f"ORD-{random_str}"


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('cod', 'Cash on Delivery'),
        ('razorpay', 'Razorpay'),
        ('stripe', 'Stripe'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=50, unique=True, default=generate_order_id)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    payment_status = models.CharField(max_length=20, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='cod')
    shipping_address = models.TextField()
    phone = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.order_id

    class Meta:
        ordering = ['-created_at']


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    def get_total(self):
        return self.price * self.quantity
