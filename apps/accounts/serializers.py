from rest_framework import serializers
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


    def validate_username(self,value):
        if len(value.strip())< 3:
            raise serializers.ValidationError(
                "User name must be at least 3 character long.."
            )
        return value

    def validate_phone_number(self, value):
        if not value.isdigit():
            raise serializers.ValidationError(
                "Phone number must contain only digits."
            )

        if len(value) != 10:
            raise serializers.ValidationError(
                "Phone number must be 10 digits."
            )

        return value


    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError(
                "Passwords don't match."
            )

        if not data["accept_terms"]:
            raise serializers.ValidationError(
                "You must accept terms for registration."
            )

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


class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()  #user id from the reset link URL
    token = serializers.CharField() #security token yo chai email user kai ho vanera thaa pauna

    password = serializers.CharField(write_only=True,min_length=8)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self,data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError(    # error confirm password muni aaucha yo garea pachi
                {"confirm_password" : "Password do not match."}
            )
        return data


# Serializer for user login with username and password
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


# Serializer for user logout using refresh token only
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(write_only=True)  


class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True)


    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "phone_number",
            "favourite_games",
            "is_staff",
            "is_superuser",
        ]