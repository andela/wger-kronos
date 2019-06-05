from django.core.management.base import (
    BaseCommand,
    CommandError
)
from django.contrib.auth.models import User
from wger.core.models import UserProfile
from rest_framework.authtoken.models import Token


class Command(BaseCommand):

    help = 'Creates user using api key '

    def add_arguments(self, parser):
        parser.add_argument('api_key', type=str)
        parser.add_argument('creator_username', type=str)

    def handle(self, *args, **options):
        try:
            api_key = Token.objects.filter(key=options['api_key'])
            created_by = User.objects.filter(username=options['creator_username'])
            if not (created_by.exists() and api_key.exists()):
                self.stdout.write(self.style.ERROR('Invalid access, try again'))
            profile = UserProfile.objects.filter(user=created_by).values('is_allowed')
            if api_key and profile[0]['is_allowed']:
                self.stdout.write(self.style.ERROR('User already has access to create other users'))
            else:
                UserProfile.objects.filter(user=created_by).update(is_allowed=True)
                self.stdout.write(self.style.SUCCESS('Access granted to create api users'))
        except CommandError:
            self.stdout.CommandError(self.style.ERROR('api_key and username fields are required'))
