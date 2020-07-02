from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from bank_accounts.exceptions import AccountDoesNotExistException
from bank_accounts.models import AccountHistory, CitizenAccount
from bank_accounts.serializers import (
    CitizenAccountCreateSerializer,
    CitizenAccountDetailSerializer,
    CitizenAccountHistoryListSerializer,
    CitizenAccountListSerializer,
    CitizenAccountUpdateSerializer,
)
from citizens.exceptions import CitizenDoesNotExistException
from citizens.models import Citizen
from common_utils.mixins import GetSerializerClassMixin


class BankAccountViewSet(GetSerializerClassMixin, viewsets.ModelViewSet):
    permission_classes = (permissions.IsAdminUser,)
    queryset = CitizenAccount.objects.all()
    serializer_class = CitizenAccountListSerializer
    serializer_action_classes = {
        "create": CitizenAccountCreateSerializer,
        "list": CitizenAccountListSerializer,
        "retrieve": CitizenAccountDetailSerializer,
        "partial_update": CitizenAccountUpdateSerializer,
        "get_account_history": CitizenAccountHistoryListSerializer,
    }

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        citizen = Citizen.objects.filter(
            pk=serializer.validated_data["citizen_id"]
        ).first()
        if citizen:
            serializer.validated_data["owner"] = citizen
            self.perform_create(serializer)
            return Response(
                f"Citizen bank account for citizen: {citizen.name} {citizen.surname} has been created.",
                status=status.HTTP_201_CREATED,
            )
        else:
            raise CitizenDoesNotExistException

    def partial_update(self, request, pk=None, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        citizen_account = CitizenAccount.objects.filter(pk=pk).first()

        if citizen_account:
            amount = serializer.validated_data["amount_of_change"]
            citizen_account.account_balance += amount
            citizen_account.save()

            citizen_account.add_entry_to_operation_history(amount)

            return Response(
                f"Account balance has been changed, the amount of change is equal : {amount}, current account balance is equal: {citizen_account.account_balance}"
            )
        else:
            raise AccountDoesNotExistException

    @action(
        methods=["get"],
        detail=True,
        url_path="account-history",
        url_name="account_history",
    )
    def get_account_history(self, request, pk=None, *args, **kwargs):
        entries = AccountHistory.objects.filter(account__pk=pk)
        serializer = self.get_serializer(entries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
