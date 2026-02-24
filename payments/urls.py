from django.urls import path
from .views import (
    checkout, initiate_payment, razorpay_callback,
    stripe_payment, stripe_success, stripe_cancel,
    payment_success, payment_failed
)

urlpatterns = [
    path('checkout/', checkout, name='checkout'),
    path('checkout/<int:order_id>/', checkout, name='checkout'),
    
    # Razorpay
    path('razorpay/pay/<int:order_id>/', initiate_payment, name='initiate_payment'),
    path('razorpay/callback/', razorpay_callback, name='razorpay_callback'),
    path('razorpay/qr/<int:order_id>/', initiate_payment, name='razorpay_qr'),
    
    # Stripe
    path('stripe/pay/<int:order_id>/', stripe_payment, name='stripe_payment'),
    path('stripe/success/', stripe_success, name='stripe_success'),
    path('stripe/cancel/', stripe_cancel, name='stripe_cancel'),
    
    # Generic
    path('success/', payment_success, name='payment_success'),
    path('failed/', payment_failed, name='payment_failed'),
]
