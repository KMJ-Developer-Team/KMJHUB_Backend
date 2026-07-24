from django.contrib.auth import authenticate
from rest_framework import permissions, status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from urllib import request
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str  # forcebype for value to byte conversion(encoding garna ) arko chai decoding
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode #creates URL_Safe string , encodes user ID (dont knokw wtf this is mari mari bujna khojiya )

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from .models import User
from .serializers import (
    PasswordResetSerializer,
    PasswordResetConfirmSerializer,
    RegistrationSerializer,
    LoginSerializer, 
    LogoutSerializer,
)

# registration api view which is used to register user 
class RegistrationApiView(APIView):
    permission_classes = [permissions.AllowAny] #permission to allow any uyser to interact with register api endpoint
    try:
        def post(self, request):
            serializer= RegistrationSerializer(data=request.data) #getting data send from frontedna nd converting it in python objects

            if serializer.is_valid(): #check validation on every data by calling validate function in serializer class and create a dictionary called validated_data which include validated data
                serializer.save() # call create fucntion in serializer class 
                return Response(
                    serializer.data, status= status.HTTP_201_CREATED
                )
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)

class PasswordResetView(APIView):
    #permission diyena so aailea lai yo view ko lai permission deko
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data["email"]

            user = User.objects.filter(email=email).first()

            if user:
                token = PasswordResetTokenGenerator().make_token(user) #create the unique token, temp ho yo remember
                uid = urlsafe_base64_encode(force_bytes(user.id))  # tiyo mathi ko base64 ya use huncha encode garna id lai byte ma convert


                    # front end ko link lai point gariya 
                reset_link = (
                    f"http://localhost:5173/reset-password/{uid}/{token}"
                )
                    #self explainatory
                send_mail(
                    subject="Password Reset Request",
                    message=f"Reset your password here:\n\n{reset_link}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                )
                #aailea aalchi lagiyo try catch banauna so.
            return Response(
                {
                    "message": "If an account exists, password reset link has been sent."
                },
                status=status.HTTP_200_OK,
            )
        # in case fail
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class PasswordResetConfirmView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        uid = serializer.validated_data["uid"]  # extract gariya page ma  user ko uid token
        token = serializer.validated_data["token"]
        password = serializer.validated_data["password"]

        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.filter(id=user_id).first()
        except Exception:
            user= None


        if user is None or not PasswordResetTokenGenerator().check_token(user,token):  #user valid cha aani tiyo token ni valid cha check gariya
            return Response(
                {"error": "Invalid or expired reset link."},
                status = status.HTTP_400_BAD_REQUEST
            )

        #error aaiyena vani set password aani save
        user.set_password(password)
        user.save()

        return Response(
            {"message":"Reached this point successfully."},
            status = status.HTTP_200_OK
        )


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]   # allow any user to access this view

    def post(self, request):   # handle post request for login
        serializer = LoginSerializer(data= request.data)   
        # create a serializer instance with the request data then validate username and password
        serializer.is_valid(raise_exception=True)          
        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]
        user = authenticate(request, username=username, password=password)  

        if user is None:
            raise AuthenticationFailed("Invalid username or password")

        refresh = RefreshToken.for_user(user)   # generate a JWT refresh token for the authenticated user
        return Response({
                # convert access and refresh token to a JWT string
                "access": str(refresh.access_token),   
                "refresh": str(refresh),
                "message": "Login successful",  

                # return user details in the response for frontend
                "user": {  
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "role": user.role,
                },
            },
            status=status.HTTP_200_OK,
        )


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]   # only logged in user can call this api endpoint

    def post(self, request):
        # check if the request data contains a valid refresh token
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # get the refresh token from the request data
        refresh_token = serializer.validated_data["refresh"]  

        try:   # blacklist the refresh token to make it unusable for future requests
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError:
            return Response({"message": "Invalid or expired refresh token."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Logout successful."}, status=status.HTTP_200_OK)
