import uuid

from django.db import models

from citizens.constants import CitizenProfessionType, CitizenStatusType, MetroStationType


class Citizen(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=25, null=False)
    surname = models.CharField(max_length=40, null=False)
    place_of_resident = models.CharField(
        max_length=50, choices=MetroStationType.choices, null=False
    )
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


class CitizenFile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    citizen = models.ForeignKey(Citizen, on_delete=models.PROTECT)
    description = models.CharField(max_length=400, null=False)
    result = models.CharField(max_length=200)
    citizen_status_changed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "citizen_file"
