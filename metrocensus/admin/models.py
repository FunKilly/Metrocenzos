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


class User(AbstractBaseUser, PermissionsMixin):
    """ User model with UserRoleType choices representing role in system. """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, blank=False, unique=True, null=False)
    role = models.CharField(
        max_length=30, choices=UserRoleType.choices, default=UserRoleType.TRUSTEE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "name"

    def __str__(self):
        return self.name

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    @staticmethod
    def check_if_user_exist(email):
        return User.objects.filter(email=email).exists()
