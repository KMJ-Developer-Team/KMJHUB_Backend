from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):

    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique= True)
    phone_number = models.CharField(max_length=10, unique=True, null=True)
    role = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add= True , unique= True )
    updated_at = models.DateTimeField(auto_now_add= True,  unique = True )
    