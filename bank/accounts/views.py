from django.shortcuts import render

from rest_framework import generics, permissions, status, viewsets, mixins
from rest_framework.authentication import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework import permissions

from accounts.models import Citizen
from accounts.serializers import CitizenSerializer

class CitizenViewSet(viewsets.GenericViewSet,
    mixins.ListModelMixin,
):
    serializer_class = CitizenSerializer
    queryset = Citizen.objects.all()
