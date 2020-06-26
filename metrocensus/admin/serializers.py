from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from metrocensus.admin.exceptions import PasswordConfirmationFailedException


class UserCreationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["password", "password2", "username", "first_name", "last_name"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User(
            username=self.validated_data["username"],
            first_name=self.validated_data.get("first_name", ""),
            last_name=self.validated_data.get("last_name", ""),
            is_staff=True,
        )
        user.set_password(self.validated_data["password"])
        user.save()
        return user

    def validate(self, data):
        password = data.get("password")
        password2 = data.get("password2")

        if password != password2:
            raise PasswordConfirmationFailedException
        else:
            validate_password(password)
            return data


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["password"]


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name"]


class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
