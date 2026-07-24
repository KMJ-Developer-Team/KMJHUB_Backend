from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from rest_framework import permissions
from .serializers import ProductListSerializer, ProductDetailSerializer
from .pagination import ProductPagination


class ProductListAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        products = Product.objects.filter(is_active=True).order_by("-created_at")
        paginator = ProductPagination()
        paginated_products = paginator.paginate_queryset(products, request)
        serializer = ProductListSerializer(paginated_products, many=True)
        return paginator.get_paginated_response(serializer.data)


class ProductDetailAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, slug):
        try:
            product = Product.objects.get(slug=slug, is_active=True)
        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductDetailSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)