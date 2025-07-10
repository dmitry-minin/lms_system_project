from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group, Permission
from users.models import User


class Command(BaseCommand):
    """ Command to add a user to the moderator group. """
    
    help = "Add a user to the moderator group"

    def add_arguments(self, parser):
        parser.add_argument("email", type=str, help="Email of the user to be added to the Moderator group")

    def handle(self, *args, **options):
        email = options["email"]
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise CommandError(f"User {email} does not exist.")
        try:
            moderator_group = Group.objects.get(name="Moderator")
        except Group.DoesNotExist:
            raise CommandError("Moderator group does not exist. Please create it first.")

        user.groups.add(moderator_group)
        self.stdout.write(self.style.SUCCESS(f"User {email} added to the Moderator group."))
