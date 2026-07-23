from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import PasswordResetSerializer
# Create your views here.


class PasswordResetView(APIView):
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validate_data["email"]
            user = User.objects.filter(email=email).first()
        return Response(
            serializer,errors,
            status=status.HTTP_400_BAD_REQUEST
        )