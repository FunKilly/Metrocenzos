import uuid

from django.db import models
from accounts.constants import CitizenProfessionType, CitizenStatusType, MetroStationType


class Citizen(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=25, null=False)
    surname = models.CharField(max_length=40, null=False)
    place_of_resident = models.CharField(max_length=50,
        choices=MetroStationType.choices,
        default=MetroStationType.UNKNOWN,)
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
        db_table = "citizens_citizen"


class CitizenAccount(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(Citizen, on_delete=models.PROTECT)
    account_balance = models.DecimalField(default=0, decimal_places=2, max_digits=9)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

class AccountHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.ForeignKey(CitizenAccount, on_delete=models.PROTECT)
    description = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
