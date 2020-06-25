from django.contrib.auth.models import User
from rest_framework import generics, status

from metrocensus.admin.permissions import IsSuperAdmin
from metrocensus.admin.serializers import UserCreationSerializer


class UserCreationView(generics.CreateAPIView):
    permission_classes = (IsSuperAdmin,)
    serializer_class = UserCreationSerializer

    def create(self, request, token=None, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        user = serializer.instance
        return Response(f"Account with username: {user.username} has been created.", status=status.HTTP_201_CREATED)
    
