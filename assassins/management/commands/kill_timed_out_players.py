from django.core.management.base import BaseCommand, CommandError
from assassins.models import Player

class Command(BaseCommand):
    help = 'Kills players who have exceeded the time limit for their assassination and sends appropriate email notifications.'

    def handle(self, *args, **options):
        players = Player.objects.filter(living=True)
        for player in players:
            if player.get_time_remaining() == 0:
                self.stdout.write("Eliminating %s due to timeout" % player.full_name())
                player.die_from_timeout()
