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
        default=CitizenProfessionType.OTHER,
    )
    status = models.CharField(
        max_length=30, choices=CitizenStatusType.choices, default=CitizenStatusType.ACTIVE
    )


class CitizenFile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    desription = models.CharField(max_length=400, null=False)
    result = models.CharField(max_length=200)
    citizen_status_changed = models.BooleanField(default=False)


class ReasonOfDeath(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, null=False)
    place = models.CharField(max_length=70)
