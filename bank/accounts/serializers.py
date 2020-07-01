from rest_framework import serializers 
from accounts.models import Citizen

class CitizenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Citizen
        fields = ["name", "surname", "id"]