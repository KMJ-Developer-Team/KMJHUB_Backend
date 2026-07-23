from xml.dom import ValidationErr

from rest_framework import serializers
from .models import User

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True, min_length= 8) # this is already in model field but we use here to make it behave differently like we make write_only =true as it is false default
    confirm_password = serializers.CharField(write_only = True) #this field is not in model.py but it is used here for validation check
    accept_terms = serializers.BooleanField(write_only = True) #same as above comment

    class Meta:
        model = User
        fields= ['username', 'email', 'phone_number', 'password', 'confirm_password', 'accept_terms'] 

    def validate(self, data): #this method is called when we call serializer.is_valid() in views.py
        if data['password'] != data['confirm_password']:
            raise ValidationErr("Password don't match")

        if not data['accept_terms']:
            raise ValidationErr('You must accept terms for registration')

        return data

    def create(self, validated_data): # this method in calle when we used save() method in views.py
        validated_data.pop('confirm_password')
        validated_data.pop('accept_terms')
        user = User.objects.create_user(
            username= validated_data['username'],
            email= validated_data['email'],
            phone_number= validated_data['phone_number'],
            password= validated_data['password']
        )

        return user

        

