"""
URL configuration for ecommerce project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from products.views import home
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Home
    path('', home, name='home'),

    # Authentication
    path('accounts/', include('accounts.urls')),

    # Products
    path('products/', include('products.urls')),

    # Cart & Wishlist
    path('cart/', include('cart.urls')),

    # Orders
    path('orders/', include('orders.urls')),

    # Payments
    path('payments/', include('payments.urls')),

    # REST API
    path('api/products/', include('products.api_urls')),

    # JWT API
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
