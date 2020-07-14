
from celery import shared_task
from django.core.management import call_command


@shared_task
def calculate_interest():
    call_command("calculate_interest_command", )