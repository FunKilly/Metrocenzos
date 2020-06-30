from metrocensus.admin.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from metrocensus.admin.exceptions import PasswordConfirmationFailedException
from metrocensus.citizens.models import Citizen


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


class CitizenCreationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Citizen
        fields = ["name", "surname", "place_of_resident"]

    def create(self, validated_data):
        citizen = Citizen(
            name=self.validated_data["name"],
            surname=self.validated_data.get("surname"),
            place_of_resident=self.validated_data.get("place_of_resident"),
        )
        citizen.save()
        return citizen

class CitizenDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Citizen
        fields = '__all__'


class CitizenListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Citizen
        fields = ["id", "name", "surname", "place_of_resident", "status"]


class CitizenUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Citizen
        fields = ["place_of_resident", "profession", "status"]
