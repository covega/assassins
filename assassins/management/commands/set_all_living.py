from django.core.management.base import BaseCommand, CommandError
from assassins.models import Player

class Command(BaseCommand):
    help = 'Sets every registered player as living'

    def handle(self, *args, **options):
        players = Player.objects.all()
        for player in players:
            player.living = True
            player.save()
            self.stdout.write('Player %s set to living' % player.full_name())
