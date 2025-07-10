from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from users.models import User, Payments
from users.permissions import IsUser, IsSelf
from users.serializer import UserSerializer, PaymentSerializer, UserCreateSerializer, UserShortSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated


class UserViewSet(ListModelMixin,
                  RetrieveModelMixin,
                  UpdateModelMixin,
                  GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return UserShortSerializer
        elif self.action == 'retrieve':
            obj = self.get_object()
            if self.request.user == obj:
                return UserSerializer
            return UserShortSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ['update', 'partial_update']:
            return [IsAuthenticated(), IsSelf()]
        return [IsAuthenticated()]


class UserCreateAPIView(CreateAPIView):
    """
    View to create a new user.
    """
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class PaymentListView(ListAPIView):
    """
    View to list all payments.
    """
    queryset = Payments.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['payment_date',]
    filterset_fields = ['course', 'lesson', 'payment_method']
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        User can see only their own payments.
        """
        current_user = self.request.user
        return Payments.objects.filter(user=current_user)


class PaymentDetailView(RetrieveAPIView):
    """
    View to retrieve a specific payment by ID.
    """
    queryset = Payments.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated, IsUser]


class PaymentCreateView(CreateAPIView):
    """
    View to create a new payment.
    """
    queryset = Payments.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]


class PaymentUpdateView(UpdateAPIView):
    """
    View to update an existing payment.
    """
    queryset = Payments.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated, IsUser]


class PaymentDeleteView(DestroyAPIView):
    """
    View to delete a payment.
    """
    queryset = Payments.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated, IsUser]
