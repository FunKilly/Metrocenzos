from rest_framework import serializers

from bank_accounts.models import AccountHistory, CitizenAccount


class CitizenAccountCreateSerializer(serializers.Serializer):
    citizen_id = serializers.UUIDField()

    class Meta:
        model = CitizenAccount
        fields = []

    def create(self, validated_data):
        account = CitizenAccount(owner=self.validated_data["owner"],)
        account.save()
        return account


class CitizenAccountDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CitizenAccount
        fields = ["owner", "account_balance", "created_at", "modified_at"]


class CitizenAccountListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CitizenAccount
        fields = ["id", "owner", "created_at"]


class CitizenAccountUpdateSerializer(serializers.Serializer):
    amount_of_change = serializers.DecimalField(max_digits=9, decimal_places=2)


class CitizenAccountHistoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountHistory
        fields = "__all__"
