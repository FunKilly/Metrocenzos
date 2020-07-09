import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from users.constants import UserRoleType

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role_type = models.CharField(choices=UserRoleType.choices, max_length=20,default=UserRoleType.TRUSTEE)

    class Meta:
        db_table = "user"
