import uuid

from django.db import models

from metrocensus.citizens.constants import CitizenProfessionType, CitizenStatusType


class Location(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, null=False)


class Citizen(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=25, null=False)
    surname = models.CharField(max_length=40, null=False)
    place_of_resident = models.ForeignKey(Location, on_delete=models.PROTECT)
    profession = models.CharField(
        max_length=30,
        choices=CitizenProfessionType.choices,
        default=CitizenProfessionType.Other,
    )
    status = models.CharField(
        max_length=30, choices=CitizenStatusType.choices, default=CitizenStatusType.Active
    )


class CitizenFile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    desription = models.CharField(max_length=400, null=False)
    result = models.CharField(max_length=200)
    citizen_status_changed = models.BooleanField(default=False)


class PayoutHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    citizen = models.ForeignKey(Citizen, on_delete=models.PROTECT)
    date = models.DateField(auto_now_add=True)
    amount = models.DecimalField(default=0)


class ReasonOfDeath(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, null=False)
    place = models.CharField(max_length=70)
