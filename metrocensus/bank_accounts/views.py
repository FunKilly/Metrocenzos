from django.shortcuts import render

from rest_framework import mixins, permissions, status, viewsets
from rest_framework.authentication import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

from common_utils.mixins import GetSerializerClassMixin

class BankAccountViewSet(
    GetSerializerClassMixin,
    viewsets.ModelViewSet,)

    permission_classes = (permissions.IsAdminUser,)
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    serializer_action_classes = {
        "create": UserCreationSerializer,
        "list": UserListSerializer,
        "retrieve": UserDetailSerializer,
        "partial_update"
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