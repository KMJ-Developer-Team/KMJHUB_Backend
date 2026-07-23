from django.urls import path
from .views import RegistrationApiView
urlpatterns = [
    path('register_user/', RegistrationApiView.as_view(), name='register')
]
