from metrocensus.admin.models import User
from rest_framework import generics, permissions, status, viewsets, mixins
from rest_framework.authentication import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

from metrocensus.admin.exceptions import InvalidCredentialsException
from metrocensus.admin.mixins import GetSerializerClassMixin
from metrocensus.admin.permissions import IsSuperAdmin
from metrocensus.admin.serializers import (
    AuthTokenSerializer,
    UserCreationSerializer,
    UserDetailSerializer,
    UserListSerializer,
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

    def create(self, request, token=None, *args, **kwargs):
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
):
    permission_classes = (IsSuperAdmin,)
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    serializer_action_classes = {
        "create": UserCreationSerializer,
        "list": UserListSerializer,
        "retrieve": UserDetailSerializer,
    }