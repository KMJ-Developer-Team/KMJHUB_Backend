from django.contrib import admin
from .models import Category, Product

admin.site.register(Category)
admin.site.register(Product)
from .models import Product, Category

# Register your models here.
admin.site.register(Product)
admin.site.register(Category)

