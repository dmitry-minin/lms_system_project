from django.contrib import admin
from lms.models import Course, Lesson


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Admin interface for the Course model."""
    list_display = ("name", "description", "preview")
    search_fields = ("name", "description")
    list_filter = ("name",)
    ordering = ("name",)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """Admin interface for the Lesson model."""
    list_display = ("name", "course", "description", "preview", "video_url")
    search_fields = ("name", "description")
    list_filter = ("name", "course")
    ordering = ("name",)

    def get_queryset(self, request):
        """Override to include related course information."""
        return super().get_queryset(request).select_related('course')
