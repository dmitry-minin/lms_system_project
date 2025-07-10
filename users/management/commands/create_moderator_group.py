from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    """Command to create a moderator group with specific permissions."""

    help = 'Create a moderator group with read and update permissions'

    def handle(self, *args, **kwargs):
        moderator_group, created = Group.objects.get_or_create(name='Moderator')

        # Define the permissions to be added to the moderator group
        permissions = [
            ("lms", "change_course"),
            ("lms", "view_course"),
            ("lms", "add_course"),
            ("lms", "change_lesson"),
            ("lms", "view_lesson")
        ]

        # Add permissions to the group
        for app_label, codename in permissions:
            permission = Permission.objects.get(codename=codename, content_type__app_label=app_label)
            moderator_group.permissions.add(permission)

        self.stdout.write(self.style.SUCCESS('Moderator group created with permissions: view and update.'))
