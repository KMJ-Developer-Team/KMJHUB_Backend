from rest_framework import serializers
from .models import Product, Category


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'price', 'product_type', 'category', 'created_at']
