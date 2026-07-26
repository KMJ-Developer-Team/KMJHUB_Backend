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
            self.queryset = self.queryset.filter(product_type=product_type)

        if category:
            self.queryset = self.queryset.filter(category = category)
    
    def search(self):
        search = self.request.query_params.get("search")
        self.queryset = self.queryset.filter(Q(name__icontains = search) | Q(category__icontains = search) | Q(product_type__icontains = search))
        
    def apply(self):
        self.filter()
        self.search()
        return self.queryset
        

