from django.urls import path
from .views import order_history, order_detail, create_order, cancel_order, download_invoice

urlpatterns = [
    path('', order_history, name='order_history'),
    path('detail/<str:order_id>/', order_detail, name='order_detail'),
    path('create/', create_order, name='create_order'),
    path('cancel/<str:order_id>/', cancel_order, name='cancel_order'),
    path('invoice/<str:order_id>/', download_invoice, name='download_invoice'),
]
