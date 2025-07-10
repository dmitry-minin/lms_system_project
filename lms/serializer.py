from rest_framework.serializers import ModelSerializer, SerializerMethodField
from lms.models import Course, Lesson
from users.models import User


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    lessons_count = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    class Meta:
        model = Course
        fields = [
            "id", "name", "preview", "description", "owner", "lessons_count", "lessons"
        ]
