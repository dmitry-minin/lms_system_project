from rest_framework.serializers import ModelSerializer, SerializerMethodField, URLField
from lms.models import Course, Lesson, CourseSubscription
from lms.validators import validate_url
from users.models import User


class LessonSerializer(ModelSerializer):
    video_url = URLField(validators=[validate_url], required=False)

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    lessons_count = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    subscriptions = SerializerMethodField()

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_subscriptions(self, obj):
        request = self.context.get("request")
        user = getattr(request, "user", None)

        if user and user.groups.filter(name="Moderator").exists():
            return [
                {"user": sub.user.email}
                for sub in obj.subscriptions.all()
            ]
        elif user:
            return {"is_subscribed": obj.subscriptions.filter(user=user).exists()}
        return {"is_subscribed": False}

    class Meta:
        model = Course
        fields = [
            "id", "name", "preview", "description", "owner", "lessons_count", "lessons", "subscriptions"
        ]
        read_only_fields = ["id", "owner", "lessons_count", "subscriptions"]


class CourseSubscriptionSerializer(ModelSerializer):

    class Meta:
        model = CourseSubscription
        fields = ["user", "course"]
        read_only_fields = ["user"]
