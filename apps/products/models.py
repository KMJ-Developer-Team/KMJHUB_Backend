from django.db import models
from django.utils.text import slugify    # default product ko harek ko slug na banauna yo import 
# Create your models here.
#category -> games, movies etc etc

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,  #brute delete aailea lai 
        null = True,
        blank =True,
        related_name="children",
    )
    
    def save(self,*args,**kwargs):    # harek choti save garnu aagadhi slug banako
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    PRODUCT_TYPES = [
    ("giftcard", "Giftcard"),
    ("subscription", "Subscription"),
    ("topup","TopUp"),
    ]

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
    )

    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    image = models.ImageField(upload_to="products/", blank=True)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    stock = models.PositiveIntegerField(default=0)
    product_type = models.CharField(
        max_length=20,
        choices= PRODUCT_TYPES,
        default="giftcard",
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def stock_status(self):
        if self.stock == 0:
            return "Out of Stock"
        elif self.stock <= 10:
            return "Low Stock"
        return "In Stock"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name