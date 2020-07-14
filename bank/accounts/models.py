import uuid

from django.db import models
from accounts.constants import CitizenProfessionType, CitizenStatusType, MetroStationType
from users.models import User

class Citizen(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=25, null=False)
    surname = models.CharField(max_length=40, null=False)
    place_of_resident = models.CharField(max_length=50,
        choices=MetroStationType.choices,
        null=False)
    profession = models.CharField(
        max_length=30,
        choices=CitizenProfessionType.choices,
        default=CitizenProfessionType.UNEMPLOYED,
    )
    status = models.CharField(
        max_length=30, choices=CitizenStatusType.choices, default=CitizenStatusType.ACTIVE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    changed_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "citizen"


class CitizenAccount(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(Citizen, on_delete=models.PROTECT)
    account_balance = models.DecimalField(default=0, decimal_places=2, max_digits=9)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "citizen_account"

class AccountHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.ForeignKey(CitizenAccount, on_delete=models.PROTECT)
    description = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    transaction_support = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        db_table = "account_history"


class SavingProgramParticipant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.ForeignKey(CitizenAccount, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=4, default=0.055)
    deposit_balance = models.DecimalField(max_digits=99, decimal_places=2, default=0)
    profit = models.DecimalField(max_digits=99, decimal_places=2, default=0)

    class Meta:
        db_table = "saving_program_participant"

    def calculate_interest(self):
        profit = self.deposit_balance * self.interest_rate
        self.profit += profit
        self.save()
