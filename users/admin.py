from django.contrib import admin
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "phone", "city", "avatar", "is_staff", "is_active", "is_superuser")
    search_fields = ("email", "city", "phone")
    list_filter = ("is_staff", "is_active", "is_superuser")
    ordering = ("email",)
