from django.contrib.auth import authenticate
from rest_framework import permissions, status
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from .serializers import LoginSerializer, LogoutSerializer


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