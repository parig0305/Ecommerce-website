from django.urls import path
from .views import (
    cart_detail, add_to_cart, update_cart_item,
    remove_from_cart, clear_cart,
    wishlist, add_to_wishlist, remove_from_wishlist
)

urlpatterns = [
    path('', cart_detail, name='cart'),
    path('add/', add_to_cart, name='add_to_cart'),
    path('update/<int:item_id>/<str:action>/', update_cart_item, name='update_cart'),
    path('remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('clear/', clear_cart, name='clear_cart'),

    # Wishlist URLs
    path('wishlist/', wishlist, name='wishlist'),
    path('wishlist/add/<int:product_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:item_id>/', remove_from_wishlist, name='remove_from_wishlist'),
]
