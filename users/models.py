from django.contrib.auth.models import AbstractUser
from django.db import models


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
