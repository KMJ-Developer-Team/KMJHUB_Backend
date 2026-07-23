from urllib import request

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from .models import User
from .serializers import PasswordResetSerializer, RegistrationSerializer
# Create your views here.

# registration api view which is used to register user 
class RegistrationApiView(APIView):
    permission_classes = [AllowAny] #permission to allow any uyser to interact with register api endpoint
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