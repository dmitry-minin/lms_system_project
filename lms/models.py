from django.db import models
from config.settings import AUTH_USER_MODEL


class Course(models.Model):
    """Model representing a course in the LMS."""
    name = models.CharField(max_length=255, verbose_name="Course Name", help_text="Enter the name of the course")
    preview = models.ImageField(upload_to="lms/course_previews/", blank=True, null=True, verbose_name="Course Preview",
                                help_text="Upload a preview image for the course. Optional.")
    description = models.TextField(blank=True, null=True, verbose_name="Course Description",
                                   help_text="Enter a brief description of the course")
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="courses", blank=True, null=True,
                              verbose_name="Course Owner", help_text="Fill in the owner of the course. Optional.")
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name="Updated At",
                                      help_text="The date and time when the course was last updated")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"
        ordering = ["name"]


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
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="lessons", blank=True, null=True,
                              verbose_name="Course Owner", help_text="Fill in the owner of the course. Optional.")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Lesson"
        verbose_name_plural = "Lessons"
        ordering = ["name"]


class CourseSubscription(models.Model):
    """Model representing a subscription to a course."""
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="course_subscriptions",
                             verbose_name="User", help_text="Select the user who subscribed to the course")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="subscriptions",
                               verbose_name="Course", help_text="Select the course that the user subscribed to")

    def __str__(self):
        return f"{self.user.username} - {self.course.name}"

    class Meta:
        verbose_name = "Course Subscription"
        verbose_name_plural = "Course Subscriptions"
        unique_together = ("user", "course")
        ordering = ["user", "course"]
