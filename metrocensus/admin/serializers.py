from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from admin.exceptions import PasswordConfirmationFailedException
from admin.models import User
from citizens.constants import CitizenProfessionType, CitizenStatusType
from citizens.models import Citizen, CitizenFile


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
        fields = "__all__"


class CitizenListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Citizen
        fields = ["id", "name", "surname", "place_of_resident", "status"]


class CitizenUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Citizen
        fields = ["place_of_resident", "profession", "status"]


class CitizenFileCreateSerializer(serializers.ModelSerializer):
    citizen_status = serializers.ChoiceField(choices=CitizenStatusType, required=False)
    citizen_profession = serializers.ChoiceField(
        choices=CitizenProfessionType, required=False
    )
    result = serializers.CharField(max_length=200, required=False)

    class Meta:
        model = CitizenFile
        fields = ["description", "result", "citizen_status", "citizen_profession"]

    def create(self, validated_data):
        entry = CitizenFile(
            citizen=self.validated_data["citizen"],
            description=self.validated_data["description"],
            citizen_status_changed=self.validated_data.get(
                "citizen_status_changed", False
            ),
            result=self.validated_data.get("result"),
        )
        entry.save()
        return entry


class CitizenFileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CitizenFile
        fields = [
            "id",
            "citizen",
            "description",
            "result",
            "citizen_status_changed",
            "created_at",
        ]
