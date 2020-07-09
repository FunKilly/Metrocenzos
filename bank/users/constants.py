from django.db import models
from django.utils.translation import gettext_lazy as _


class UserRoleType(models.TextChoices):
    ADMIN = "admin", _("Admin")
    TRUSTEE = "trustee", _("Trustee")
    BANKER = "banker", _("Banker")
