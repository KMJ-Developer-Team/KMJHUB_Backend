from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Category
from .serializers import ProductListSerializer
from rest_framework import permissions


class ProductListAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        products = Product.objects.filter(is_active=True).order_by("-created_at")
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
        

