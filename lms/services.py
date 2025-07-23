from lms.models import Course
from datetime import timedelta
from django.utils import timezone


def check_if_notification_needed(current_info=None) -> tuple[bool, list]:
    """
    Check if a notification is needed for the course.
    This function checks if the course has been updated recently (more than 4 hours ago) to notify subscribers about
    updates.
    Args:
        current_info (Course): The course instance to check.
    Returns: True if a notification is needed, False otherwise and a list of email recipients.
    """
    print(current_info)
    print(current_info.subscriptions.exists())
    print(current_info.updated_at)
    print((timezone.now() - current_info.updated_at))
    if not current_info or not current_info.subscriptions.exists():
        return False, []
    elif current_info.updated_at and (timezone.now() - current_info.updated_at) > timedelta(hours=4):
        print("Notification needed")
        recipients = list(current_info.subscriptions.values_list('user__email', flat=True))
        return True, recipients
    print("No notification needed")
    return False, []
