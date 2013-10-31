from django.core.management.base import BaseCommand, CommandError

from assassins.models import email_all

class Command(BaseCommand):
      help = 'Emails everyone a message'

      def handle(self, *args, **options):
            subject = args[0]
            message = args[1]
            
            email_all(subject, message)
