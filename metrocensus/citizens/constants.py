from django.db import models
from django.utils.translation import gettext_lazy as _


class CitizenStatusType(models.TextChoices):
    ACTIVE = "active", _("Active")
    MISSING = "missing", _("Missing")
    DECEASED = "deceased", _("Deceased")
    WANTED = "wanted", _("Wanted")


class CitizenProfessionType(models.TextChoices):
    SOLDIER = "soldier", _("Soldier")
    STALKER = "stalker", _("Stalker")
    BOOKMAN = "bookman", _("Bookman")
    INTERNAL_WORKER = "internal_worker", _("Internal Worker")
    OTHER = "other", _("Other")
    UNEMPLOYED = "unemployed", _("Unemployed")
    COMMANDER = "commander", _("Commander")
    SHOPKEEPER = "shopkeeper", _("Shopkeeper")
