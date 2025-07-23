from celery import shared_task
from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER
from lms.models import Course
from users.models import User
from django.utils import timezone
from datetime import timedelta


@shared_task
def send_course_update_email(recipients, course_name, updated_data):
    """
    Send an email notification to the course subscribers about the course update.
    """
    model = Course

    change_messages = []
    for field_name, new_value in updated_data.items():
        # Получить verbose_name поля
        field = model._meta.get_field(field_name)
        verbose_name = field.verbose_name

        change_messages.append(f"• {verbose_name}: {new_value}")

    changes_text = "\n".join(change_messages)

    subject = f"Курс '{course_name}' обновлен"
    message = f"""
        Курс "course_name" был обновлен.

        Изменения:
        {changes_text}
        """
    send_mail(subject, message, EMAIL_HOST_USER, recipients)


@shared_task
def deactivate_not_active_users():
    """
    Deactivate users who have not been active for a month or more.
    This task can be scheduled to run periodically.
    """
    cutoff_date = timezone.now() - timedelta(days=30)
    users_old_login = User.objects.filter(
        is_active=True,
        last_login__lt=cutoff_date
    )
    users_never_logged_in = User.objects.filter(
        is_active=True,
        date_joined__lt=cutoff_date,
        last_login__isnull=True
    )
    for user in users_old_login:
        user.is_active = False
        user.save()
        print(f"User {user.email} has been deactivated due to inactivity.")

    for user in users_never_logged_in:
        user.is_active = False
        user.save()
        print(f"User {user.email} has been deactivated due to never logging in.")
