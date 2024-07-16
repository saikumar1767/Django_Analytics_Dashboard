from django.core.management.base import BaseCommand
from api.models import User

class Command(BaseCommand):
    help = 'Remove a user with a specific ID'

    def handle(self, *args, **kwargs):
        try:
            user = User.objects.get(id=5)
            user.delete()
            self.stdout.write(self.style.SUCCESS('Successfully deleted user with ID 1'))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('User with ID 1 does not exist'))
