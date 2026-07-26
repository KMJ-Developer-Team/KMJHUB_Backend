from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status
from .models import Product
from .filters import FilterAndSearch
# Create your views here.

class FilterAndSearchView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        try:
            queryset = Product.objects.all()
            product_filter = FilterAndSearch(queryset, request)
            product_filter - product_filter.apply()
            return Response()
        except:
            return Response(
                {"message": "Data not available"}, 
                status=status.HTTP_204_NO_CONTENT
            )
