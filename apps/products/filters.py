from rest_framework.views import APIView
from django.db.models import Q


class FilterAndSearch:
    # this contructor is used because we can use only self as a parameter in all method inside this class if we don't use init constructor then we have pass request and queryset to every method as parameter
    def __init__(self, request, queryset): #contructor which is called when object is created in views
        self.request = request #it store incoming request
        self.queryset = queryset # it store queryset pass down from views.py

    def filter(self):
        product_type = self.request.query_params.get("product_type") #it fetch the value of product_type from url
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
                Q(name__icontains=search_type) | # Q allow to use complex operation such as or , and operation
                Q(category__name__icontains=search_type) | 
                Q(product_type__icontains=search_type)
            )
        
    def apply(self):
        self.filter()
        self.search()
        return self.queryset
        

