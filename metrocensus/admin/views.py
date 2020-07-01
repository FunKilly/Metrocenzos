from admin.models import User
from rest_framework import generics, permissions, status, viewsets, mixins
from rest_framework.authentication import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework import permissions

from citizens.models import Citizen, CitizenFile
from admin.exceptions import InvalidCredentialsException
from admin.mixins import GetSerializerClassMixin
from admin.permissions import IsSuperAdmin
from admin.serializers import (
    AuthTokenSerializer,
    UserCreationSerializer,
    UserDetailSerializer,
    UserListSerializer,
    CitizenCreationSerializer,
    CitizenDetailSerializer,
    CitizenListSerializer,
    CitizenUpdateSerializer
)


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

    def get_user_if_valid(self, data):
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
        "partial_update": CitizenUpdateSerializer,
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


#class CitizenFileUpdateView(generics.UpdateAPIView):
