

from rest_framework import serializers
from bank_accounts.models import CitizenAccount

class CitizenAccountCreateSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()

    class Meta:
        model = CitizenAccount
        fields = []

    def create(self, validated_data):
        account = CitizenAccount(
            owner=self.validated_data["owner"],
        )
        account.save()
        return account


class CitizenAccountDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CitizenAccount
        exclude = ["owner", "account_balance", "created_at", "modified_at"]


class CitizenAccountListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CitizenAccount
        fields = ["owner", "created_at"]


class CitizenAccountUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CitizenAccount
        fields = ["account_balance"]