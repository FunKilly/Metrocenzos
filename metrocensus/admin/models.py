import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from citizens.models import Citizen


class PayoutHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    citizen = models.ForeignKey(Citizen, on_delete=models.PROTECT)
    date = models.DateField(auto_now_add=True)
    amount = models.DecimalField(default=0, decimal_places=2, max_digits=9)

    class Meta:
        db_table = "payout_history"


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        db_table = "user"

