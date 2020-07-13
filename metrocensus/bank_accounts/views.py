from rest_framework import permissions, status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from bank_accounts.exceptions import AccountDoesNotExistException
from bank_accounts.models import AccountHistory, CitizenAccount, SavingProgramParticipant
from bank_accounts.serializers import (
    CitizenAccountCreateSerializer,
    CitizenAccountDetailSerializer,
    CitizenAccountHistoryListSerializer,
    CitizenAccountListSerializer,
    CitizenAccountUpdateSerializer,
    SavingProgramCreateSerializer,
    SavingProgramDetailSerializer,
    SavingProgramListSerializer
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
            id=serializer.validated_data["citizen_id"]
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

        citizen_account = CitizenAccount.objects.filter(id=pk).first()

        if citizen_account:
            amount = serializer.validated_data["amount_of_change"]
            citizen_account.account_balance += amount
            citizen_account.save()

            citizen_account.add_entry_to_operation_history(amount, request.user)

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
        entries = AccountHistory.objects.filter(account__id=pk)
        serializer = self.get_serializer(entries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SavingProgramViewSet(GetSerializerClassMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    permission_classes = (permissions.IsAdminUser,)
    queryset = SavingProgramParticipant.objects.all()
    serializer_class = SavingProgramListSerializer
    serializer_action_classes = {
        "retrieve": SavingProgramDetailSerializer,
        "create": SavingProgramCreateSerializer,
    }

    def retrieve(self, request, pk=None, *args, **kwargs):
        program = SavingProgramParticipant.objects.filter(account__id=pk).first()
        if program:
            serializer = self.get_serializer(program)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response("Saving program does not exist.", status=status.HTTP_400_BAD_REQUEST)


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        account = CitizenAccount.objects.filter(id=serializer.validated_data["account_id"]).first()

        if self.operation_is_valid(serializer.validated_data, account.account_balance):

            saving_program = SavingProgramParticipant(account=account)
            saving_program.save()

            self.transfer_money(saving_program, account, serializer.validated_data["deposit_balance"])
            return Response("Saving program for an account has been created.", status=status.HTTP_201_CREATED)
        else:
            return Response("Operation is invalid, saving program already exists, account with given id does not exist or account balance is too low.")

    def operation_is_valid(self, data, account_balance):
            if data["deposit_balance"] > account_balance:
                return False
            elif SavingProgramParticipant.objects.filter(account__id=data["account_id"]).exists():
                return False
            else:
                return True
    
    def transfer_money(self, saving_program, account, deposit_balance):
        saving_program.deposit_balance = deposit_balance
        saving_program.save()

        account.account_balance -= deposit_balance
        account.save()

    def get_account_history(self, request, pk=None, *args, **kwargs):
        entries = AccountHistory.objects.filter(account__id=pk)
        serializer = self.get_serializer(entries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=["delete"],
        detail=True,
        url_path="deactivate-program",
        url_name="deactivate_program",
    )
    def deactivate_program(self, request, pk=None, *args, **kwargs):
        program = SavingProgramParticipant.objects.filter(account__id=pk).first()
        if program:
            account = CitizenAccount.objects.filter(id=pk).first()

            self.withdraw_money(program, account)
            program.delete()

            return Response("Saving program has been closed, profit has been transfered", status=status.HTTP_200_OK)
        else:
            return Response("Saving program does not exist.", status=status.HTTP_400_BAD_REQUEST)

    def withdraw_money(self, saving_program, account):
        total_sum = saving_program.deposit_balance + saving_program.profit

        account.account_balance += total_sum
        account.save()


                

