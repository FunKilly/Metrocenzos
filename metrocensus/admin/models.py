import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from metrocensus.admin.constants import UserRoleType
from metrocensus.citizens.models import Citizen


class PayoutHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    citizen = models.ForeignKey(Citizen, on_delete=models.PROTECT)
    date = models.DateField(auto_now_add=True)
    amount = models.DecimalField(default=0, decimal_places=2, max_digits=9)


class WealthStatus(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    currency = models.CharField(max_length=30, null=False)
    default = models.BooleanField(default=False)
    converter = models.DecimalField(decimal_places=2, default=0, max_digits=9)
