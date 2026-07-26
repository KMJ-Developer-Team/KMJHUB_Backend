from django.urls import path
from .views import RegistrationApiView
from .views import LoginView, LogoutView
from .views import PasswordResetView,PasswordResetConfirmView
from .views import UserProfileView
urlpatterns = [
    path('register_user/', RegistrationApiView.as_view(), name='register'),
    path("password-reset/", PasswordResetView.as_view(), name="password-reset"),
    path("password-reset-confirm/",PasswordResetConfirmView.as_view(),name="password-reset-confirm",),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", UserProfileView.as_view(), name="profile")

]
