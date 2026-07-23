from rest_framework import serializers

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

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