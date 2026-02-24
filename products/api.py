from rest_framework import serializers, viewsets
from .models import Product, ProductVariant


class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['id', 'size', 'color', 'stock']


class ProductSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'image', 'variants']


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        queryset = Product.objects.all()
        
        # Search
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search)
        
        # Category filter
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__iexact=category)
        
        # Price filter
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        return queryset
