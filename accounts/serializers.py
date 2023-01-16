from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User


class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={"inpyt_type": "password"})

    class Meta:
        model = User
        fields = ["pk", "username", "email", "password", "confirm_password"]
        extra_kwargs = {
            "password": {"write_only": True},
            "confirm_password": {"write_only": True},
        }

    def validate(self, data):
        password = data["password"]
        confirm_password = data.pop("confirm_password")

        if password != confirm_password:
            raise serializers.ValidationError(
                "password and confirm password not matched."
            )

        # encrypt and saving password
        encrypted_password = make_password(password)
        data["password"] = encrypted_password
        return super().validate(data)
