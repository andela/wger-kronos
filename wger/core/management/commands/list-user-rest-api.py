from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from wger.core.models import UserModel
from tabulate import tabulate


class Command(BaseCommand):

    help = 'Get all users created via the API'

    def add_arguments(self, parser):
        parser.add_argument('creator_username', type=str)

    def handle(self, *args, **options):
        try:
            user = User.objects.filter(username=options['creator_username'])
            if not user.exists():
                self.stdout.write(self.style.ERROR('username not found'))
            created_members = UserModel.objects.filter(
                created_by=user).values_list(
                'api_user__username', 'created_by__username')
            self.stdout.write(
                self.style.MIGRATE_HEADING(
                    tabulate(
                        created_members,
                        headers=[
                            "USER",
                            "CREATED_BY"],
                        tablefmt="github")))
        except CommandError:
            self.stdout.write(self.style.ERROR('username field is required'))
