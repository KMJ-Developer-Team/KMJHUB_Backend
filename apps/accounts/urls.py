from django.urls import path
from .views import RegistrationApiView
from .views import PasswordResetView,PasswordResetConfirmView

urlpatterns = [
    path('register_user/', RegistrationApiView.as_view(), name='register'),
    path("password-reset/", PasswordResetView.as_view(), name="password-reset"),
    path("password-reset-confirm/",PasswordResetConfirmView.as_view(),name="password-reset-confirm",),
]
