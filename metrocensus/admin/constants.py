from django.db import models
from django.utils.translation import gettext_lazy as _


class UserRoleType(models.TextChoices):
    ADMINISTRATOR = "administrator", _("Administrator")
    TRUSTEE = "trustee", _("Missing")
    DECEASED = "deceased", _("Deceased")
    WANTED = "wanted", _("Wanted")
