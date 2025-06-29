from django.db import models


class Course(models.Model):
    """Model representing a course in the LMS."""
    name = models.CharField(max_length=255, verbose_name="Course Name", help_text="Enter the name of the course")
    preview = models.ImageField(upload_to="lms/course_previews/", blank=True, null=True, verbose_name="Course Preview",
                                help_text="Upload a preview image for the course. Optional.")
    description = models.TextField(blank=True, null=True, verbose_name="Course Description",
                                   help_text="Enter a brief description of the course")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"
        ordering = ['name']


class Lesson(models.Model):
    """Model representing a lesson in a course."""
    name = models.CharField(max_length=255, verbose_name="Lesson Name", help_text="Enter the name of the lesson")
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, blank=True, null=True, related_name="lessons",
                               verbose_name="Course", help_text="Select the course this lesson belongs to")
    description = models.TextField(blank=True, null=True, verbose_name="Lesson Description",
                                   help_text="Enter a brief description of the lesson. Optional.")
    preview = models.ImageField(upload_to="lms/lesson_previews/", blank=True, null=True, verbose_name="Lesson Preview",
                                help_text="Upload a preview image for the lesson. Optional.")
    video_url = models.URLField(blank=True, null=True, verbose_name="Video URL",
                                help_text="Enter the URL of the lesson video. Optional.")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Lesson"
        verbose_name_plural = "Lessons"
        ordering = ['name']
