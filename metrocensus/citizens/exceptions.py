from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions, status


class CitizenDoesNotExistException(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("Citizen does not exist.")
    default_code = "citizen_does_not_exist"
