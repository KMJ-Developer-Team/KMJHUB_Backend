from rest_framework.views import APIView
from django.db.models import Q


class FilterAndSearch:

    def __init__(self, request, queryset):
        self.request = request
        self.queryset = queryset

    def filter(self):
        product_type = self.request.query_params.get("product_type")
        category= self.request.query_params.get("category")

        if product_type:
            self.queryset = self.queryset.filter(product_type__icontains=product_type)

        if category:
            self.queryset = self.queryset.filter(category__name__icontains= category)
    
    def search(self):
        search_type = self.request.query_params.get("search_type")
        print("Search:", search_type)

        if search_type:
            self.queryset = self.queryset.filter(
                Q(name__icontains=search_type) | 
                Q(category__name__icontains=search_type) | 
                Q(product_type__icontains=search_type)
            )
        
    def apply(self):
        self.filter()
        self.search()
        return self.queryset
        

