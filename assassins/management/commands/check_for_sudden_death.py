from django.core.management.base import BaseCommand, CommandError
from assassins.models import Player, Dorm, send_sudden_death_message

class Command(BaseCommand):
    help = 'Checks if a dorm should switch over to sudden death'

    def handle(self, *args, **options):
        dorms = Dorm.objects.all()
        for dorm in dorms:
            if (not dorm.game_started) or dorm.sudden_death: 
                continue

            if dorm.get_sudden_death_countdown_remaining() == 0:
                self.stdout.write("Converting %s to sudden death" % dorm.name)
                dorm.sudden_death = True
                dorm.sudden_death_countdown = None
                dorm.save()
                send_sudden_death_message(dorm)
