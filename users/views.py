from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from users.models import User, Payments
from users.serializer import UserSerializer, PaymentSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend


class UserViewSet(ListModelMixin,
                  RetrieveModelMixin,
                  UpdateModelMixin,
                  GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PaymentListView(ListAPIView):
    """
    View to list all payments.
    """
    queryset = Payments.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['payment_date',]
    filterset_fields = ['course', 'lesson', 'payment_method']


class PaymentDetailView(RetrieveAPIView):
    """
    View to retrieve a specific payment by ID.
    """
    queryset = Payments.objects.all()
    serializer_class = PaymentSerializer


class PaymentCreateView(CreateAPIView):
    """
    View to create a new payment.
    """
    queryset = Payments.objects.all()
    serializer_class = PaymentSerializer


class PaymentUpdateView(UpdateAPIView):
    """
    View to update an existing payment.
    """
    queryset = Payments.objects.all()
    serializer_class = PaymentSerializer


class PaymentDeleteView(DestroyAPIView):
    """
    View to delete a payment.
    """
    queryset = Payments.objects.all()
    serializer_class = PaymentSerializer
