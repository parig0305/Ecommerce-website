from django.db import models
from django.contrib.auth.models import User
from products.models import Product, ProductVariant


class Cart(models.Model):
    """Shopping cart - user-based or session-based"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='carts')
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.user:
            return f"Cart ({self.user.username})"
        return f"Cart ({self.session_key})"

    def get_total(self):
        total = 0
        for item in self.items.all():
            total += item.get_total()
        return total

    def get_item_count(self):
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    """Item in shopping cart"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    def get_total(self):
        price = self.variant.product.price if self.variant else self.product.price
        return price * self.quantity


class Wishlist(models.Model):
    """User's wishlist"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
