from django.urls import path
from .views import home, products, product_detail, category_products

urlpatterns = [
    path('', home, name='home'),
    path('products/', products, name='products'),
    path('product/<int:id>/', product_detail, name='product_detail'),
    path('category/<str:category>/', category_products, name='category_products'),
]
