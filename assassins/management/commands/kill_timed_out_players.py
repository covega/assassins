from django.core.management.base import BaseCommand, CommandError
from assassins.models import Player

class Command(BaseCommand):
    help = 'Kills players who have exceeded the time limit for their assassination and sends appropriate email notifications.'

    def handle(self, *args, **options):
        players = Player.objects.filter(living=True)
        for player in players:
            # Don't time people out if it's the final 2
            nLivingPlayers = Player.objects.filter(living=True, dorm=player.dorm).count()
            if nLivingPlayers <= 2:
                continue

            if (not player.dorm.game_started) or player.dorm.sudden_death:
                continue

            if player.get_time_remaining() == 0:
                self.stdout.write("Eliminating %s due to timeout" % player.full_name())
                player.die_from_timeout()
