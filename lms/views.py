from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from lms.paginators import CustomPageNumberPagination
from users.permissions import IsModerator, IsOwner

from lms.models import Course, Lesson, CourseSubscription
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, \
    GenericAPIView, get_object_or_404

from lms.serializer import CourseSerializer, LessonSerializer, CourseSubscriptionSerializer


class CourseViewSet(ModelViewSet):
    """
    A viewset for viewing and editing course instances.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        """ Retrieve the queryset based on the user's permissions.
        If the user is a moderator, return all courses; otherwise, return only the courses owned by the user.
        """
        user = self.request.user
        if IsModerator().has_permission(self.request, self):
            return Course.objects.all()
        return Course.objects.filter(owner=user)

    def get_permissions(self):
        """
        Assign permissions based on the action being performed.
        """
        if self.action in ["create"]:
            return [permission() for permission in self.permission_classes + [~IsModerator]]
        elif self.action in ["update", "partial_update"]:
            return [permission() for permission in self.permission_classes + [IsOwner | IsModerator]]
        elif self.action in ["destroy"]:
            return [permission() for permission in self.permission_classes + [IsOwner]]
        else:
            return [permission() for permission in self.permission_classes + [IsModerator | IsOwner]]

    def perform_create(self, serializer):
        """
        Override the create method to set the owner of the course to the current user.
        """
        serializer.save(owner=self.request.user)


class LessonListAPIView(ListAPIView):
    """
    A view to list all lessons.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        """ Retrieve the queryset based on the user's permissions.
        If the user is a moderator, return all lessons; otherwise, return only the lessons owned by the user.
        """
        user = self.request.user
        if IsModerator().has_permission(self.request, self):
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)


class LessonRetrieveAPIView(RetrieveAPIView):
    """
    A view to retrieve a specific lesson by its ID.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonCreateAPIView(CreateAPIView):
    """
    A view to create a new lesson.
    """
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]

    def perform_create(self, serializer):
        """
        Override the create method to set the owner of the course to the current user.
        """
        serializer.save(owner=self.request.user)


class LessonUpdateAPIView(UpdateAPIView):
    """
    A view to update an existing lesson.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonDestroyAPIView(DestroyAPIView):
    """
    A view to delete a lesson.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class CourseSubscriptionAPIView(GenericAPIView):
    """
    A view to handle course subscriptions.
    """
    queryset = CourseSubscription.objects.all()
    serializer_class = CourseSubscriptionSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests to create a course subscription.
        """
        user = request.user
        course_id = request.data.get("course")
        if not course_id:
            return Response({"error": "Course ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        course_item = get_object_or_404(Course, id=course_id)
        subs_item = CourseSubscription.objects.filter(user=user, course=course_item)
        if subs_item.exists():
            subs_item.delete()
            message = "Your subscription deleted successfully."
            return Response({"message": message}, status=status.HTTP_204_NO_CONTENT)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=user, course=course_item)
            message = f"You subscribed to the course '{course_item.name}' successfully."
            return Response({"message": message}, status=status.HTTP_201_CREATED)


