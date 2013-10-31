from django.core.management.base import BaseCommand, CommandError
from django.utils.timezone import now
from assassins.models import Player

from random import shuffle

class Command(BaseCommand):
    help = 'Assigns targets for every registered living player'

    def handle(self, *args, **options):
        players = list(Player.objects.filter(living=True))

        shuffle(players)

        # Null out any previous assignments for each player
        self.stdout.write('Clearing all previous assignments...')
        for player in players:
            player.target = None
            player.save()

        # Assign targets to each player
        for index, player in enumerate(players[:-1]):
            target = players[index + 1]
            self.stdout.write('Assigning %s target: %s' % (player.full_name(), target.full_name()))

            player.target = target
            player.assign_time = now()#.replace(tzinfo=utc)
            player.save()
        
        # Wrap end of list back around to the beginning to complete cycle
        player = players[-1]
        target = players[0]
        self.stdout.write('Assigning %s target: %s' % (player.full_name(), target.full_name()))

        player.target = target
        player.save()
