from rest_framework import mixins, permissions, status, viewsets
from rest_framework.authentication import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.response import Response

from admin.exceptions import InvalidCredentialsException
from admin.models import User
from admin.permissions import IsSuperAdmin
from admin.serializers import (
    AuthTokenSerializer,
    CitizenCreationSerializer,
    CitizenDetailSerializer,
    CitizenFileCreateSerializer,
    CitizenFileListSerializer,
    CitizenListSerializer,
    CitizenUpdateSerializer,
    UserCreationSerializer,
    UserDetailSerializer,
    UserListSerializer,
)
from citizens.models import Citizen, CitizenFile
from common_utils.mixins import GetSerializerClassMixin


class UserViewSet(
    GetSerializerClassMixin,
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
):
    permission_classes = (IsSuperAdmin,)
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    serializer_action_classes = {
        "create": UserCreationSerializer,
        "list": UserListSerializer,
        "retrieve": UserDetailSerializer,
    }

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        user = serializer.instance
        return Response(
            f"Account with username: {user.username} has been created.",
            status=status.HTTP_201_CREATED,
        )


class CreateTokenView(ObtainAuthToken):
    """ Create a new auth token for an user  """

    serializer_class = AuthTokenSerializer
    permission_classes = (permissions.AllowAny,)
    serializer_action_classes = {
        "create": AuthTokenSerializer,
    }

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = self.get_user_if_valid(serializer.validated_data)

        token, _ = Token.objects.get_or_create(user=user)

        return Response({"token": token.key})

    @staticmethod
    def get_user_if_valid(data):
        username = data["username"]
        password = data["password"]

        user = authenticate(username=username, password=password)

        if not user:
            raise InvalidCredentialsException
        else:
            return user


class CitizenViewSet(
    GetSerializerClassMixin,
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
):
    permission_classes = (permissions.IsAdminUser,)
    queryset = Citizen.objects.all()
    serializer_class = CitizenListSerializer
    serializer_action_classes = {
        "create": CitizenCreationSerializer,
        "list": CitizenListSerializer,
        "retrieve": CitizenDetailSerializer,
        "get_citizen_file": CitizenFileListSerializer,
        "add_entry_to_citizen_file": CitizenFileCreateSerializer,
    }

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        citizen = serializer.instance

        return Response(
            f"Account with username: {citizen.name} {citizen.surname} has been created.",
            status=status.HTTP_201_CREATED,
        )

    @action(
        methods=["get"],
        detail=True,
        url_path="retrieve-citizen-file",
        url_name="retrieve_citizen_file",
    )
    def get_citizen_file(self, request, pk=None, *args, **kwargs):
        entries = CitizenFile.objects.filter(citizen__pk=pk)
        serializer = self.get_serializer(entries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=["post"],
        detail=True,
        url_path="add-citizen-file",
        url_name="add_citizen_file",
    )
    def add_entry_to_citizen_file(self, request, pk=None, *args, **kwargs):
        citizen = Citizen.objects.filter(pk=pk).first()

        if citizen:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            if self.status_has_been_changed(serializer.validated_data, citizen):
                serializer.validated_data["citizen_status_changed"] = True
                serializer.validated_data[
                    "result"
                ] = f"Citizen status has been changed from {citizen.status} to {serializer.validated_data['citizen_status']}"

                self.change_citizen_status(
                    serializer.validated_data["citizen_status"], citizen
                )

            if self.profession_has_been_changed(serializer.validated_data, citizen):
                serializer.validated_data[
                    "result"
                ] = f"Citizen profession has been changed from {citizen.profession} to {serializer.validated_data['citizen_profession']}"

                self.change_citizen_profession(
                    serializer.validated_data["citizen_profession"], citizen
                )

            if self.resident_has_been_changed(serializer.validated_data, citizen):
                serializer.validated_data[
                    "result"
                ] = f"Citizen resident has been changed from {citizen.place_of_resident} to {serializer.validated_data['citizen_resident']}"

                self.change_citizen_resident(
                    serializer.validated_data["citizen_resident"], citizen
                )

            serializer.validated_data["citizen"] = citizen

            self.perform_create(serializer)

            return Response(
                f"Created entry in citizen file, for citizen: {citizen.name} {citizen.surname}",
                status=status.HTTP_200_OK,
            )

    def status_has_been_changed(self, data, citizen):
        if data.get("citizen_status") and data.get("citizen_status") != citizen.status:
            return True

    def change_citizen_status(self, status, citizen):
        citizen.status = status
        citizen.save()

    def profession_has_been_changed(self, data, citizen):
        if (
            data.get("citizen_profession")
            and data.get("citizen_profession") != citizen.profession
        ):
            return True

    def change_citizen_profession(self, profession, citizen):
        citizen.profession = profession
        citizen.save()
