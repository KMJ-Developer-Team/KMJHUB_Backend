from rest_framework import serializers


from .models import Product


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id', 
            'name',
            'slug',
            'price',
            'product_type',
            'image',
            'category',
            "stock",
            "stock_status",
            'created_at',

        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "price",
            "product_type",
            "category",
            "stock",
            "stock_status",
            "created_at",
            "description",
            "image",
        ]
