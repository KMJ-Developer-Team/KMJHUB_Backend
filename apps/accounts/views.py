from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str  # forcebype for value to byte conversion(encoding garna ) arko chai decoding
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode #creates URL_Safe string , encodes user ID (dont knokw wtf this is mari mari bujna khojiya )

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny


from .models import User
from .serializers import (
    PasswordResetSerializer,
    PasswordResetConfirmSerializer,
)


class PasswordResetView(APIView):
    #permission diyena so aailea lai yo view ko lai permission deko
    permission_classes = [AllowAny]

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
    permission_classes = [AllowAny]

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