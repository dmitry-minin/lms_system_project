from django.contrib.auth.models import AbstractUser
from django.db import models
from lms.models import Course, Lesson


class User(AbstractUser):
    """
    Custom user model
    """
    username = None
    email = models.EmailField(unique=True, verbose_name="email address",
                              help_text="Required. Enter a valid email address.")
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name="phone number",
                             help_text="Optional. Enter a valid phone number.")
    city = models.CharField(max_length=150, blank=True, null=True, verbose_name="city",
                            help_text="Optional. Enter your city.")
    avatar = models.ImageField(upload_to="users/avatars/", blank=True, null=True, verbose_name="avatar",
                               help_text="Optional. Upload an avatar image.")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
        ordering = ["email"]


class Payments(models.Model):
    """
    Model representing a payment made by a user.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments", verbose_name="user",
                             help_text="Select the user who made the payment.")
    payment_date = models.DateField(auto_now_add=True, verbose_name="payment date",
                                    help_text="The date when the payment was made.")
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, blank=True, null=True, related_name="payments",
                               verbose_name="course", help_text="Select the course for which the payment was made.")
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, blank=True, null=True, related_name="payments",
                               verbose_name="lesson",
                               help_text="Select the lesson for which the payment was made. Optional.")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="amount",
                                 help_text="Enter the amount of the payment.")
    payment_method = models.CharField(max_length=100, blank=True, null=True, verbose_name="payment method",
                                      help_text="Select the method of payment.")
    payment_status = models.CharField(max_length=50, blank=True, null=True, verbose_name="payment status")
    session_id = models.CharField(max_length=255, blank=True, null=True, verbose_name="session ID")
    link = models.URLField(max_length=400, blank=True, null=True, verbose_name="payment link")

    def __str__(self):
        course_name = self.course.name if self.course else None
        lesson_name = self.lesson.name if self.lesson else None
        return (f"Payment from {self.user.email} - {course_name or lesson_name} - "
                f"{self.amount} {self.payment_method}")

    class Meta:
        verbose_name = "payment"
        verbose_name_plural = "payments"
        ordering = ["-payment_date"]  # Most recent payments first
