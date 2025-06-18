from lms.models import Course, Lesson
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView

from lms.serializer import CourseSerializer, LessonSerializer


class CourseViewSet(ModelViewSet):
    """
    A viewset for viewing and editing course instances.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class LessonListAPIView(ListAPIView):
    """
    A view to list all lessons.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonRetrieveAPIView(RetrieveAPIView):
    """
    A view to retrieve a specific lesson by its ID.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonCreateAPIView(CreateAPIView):
    """
    A view to create a new lesson.
    """
    serializer_class = LessonSerializer


class LessonUpdateAPIView(UpdateAPIView):
    """
    A view to update an existing lesson.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonDestroyAPIView(DestroyAPIView):
    """
    A view to delete a lesson.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
