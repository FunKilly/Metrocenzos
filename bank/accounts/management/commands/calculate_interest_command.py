from django.core.management.base import BaseCommand, CommandError
from accounts.models import SavingProgramParticipant

class Command(BaseCommand):
    help = "Calculating profit for saving programs."

    def handle(self, *args, **options):
        self.stdout.write("Interest calculating has been launched.")

        saving_programs = SavingProgramParticipant.objects.all()
        
        for program in saving_programs:
            program.calculate_interest()

        