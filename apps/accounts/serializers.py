from rest_framework import serializers

# Serializer for user login with username and password
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

# Serializer for user logout using refresh token only
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(write_only=True)  
