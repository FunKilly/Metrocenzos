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


class MetroStationType(models.TextChoices):
    ALEKSJEJEWSKA = "alexeyevskaya", _("Alexeyevskaya")
    KIJOWSKA = "kievskaya", _("Kievskaya")
    PAVLETSKAYA = "paveletskaya", _("Paveletskaya")
    KREMLIN = "kremlin", _("Kremlin")
    POLIS = "polis", _("polis")
    RIZHSKAYA = "rizhskaya", _("Rizhskaya")
    SEVASTOPOLSKAKYA = "sevastopolskaya", _("Sevastopolskaya")
    SMOLENSKAYA = "smolenskaya", _("Smolenskaya")
    DEPOT = "depot", _("Depot")
    LUBYANKA = "lubyanka", _("Lubyanka")
    UNKNOWN = "unknown", _("Unknown")
