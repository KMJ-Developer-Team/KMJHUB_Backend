from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import permissions, authentication

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = [authentication.SessionAuthentication]

    def get(self, request):
        return Response({"message": "Login successful"})