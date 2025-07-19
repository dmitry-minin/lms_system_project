from django.db import transaction
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from users.models import User, Payments
from users.permissions import IsUser, IsSelf, IsModerator
from users.serializer import UserSerializer, PaymentSerializer, UserCreateSerializer, UserShortSerializer, \
    PaymentUpdateSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from users.services import create_price, create_session, product, retrieve_checkout_session


class UserViewSet(ListModelMixin,
                  RetrieveModelMixin,
                  UpdateModelMixin,
                  GenericViewSet):
    """
    Viewset for a User model.
    Supports list, retrieve, update and partial update actions.
    """
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
        Moderators can see all payments.
        """
        current_user = self.request.user
        if IsModerator().has_permission(self.request, self):
            return Payments.objects.all()
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

    def perform_create(self, serializer):
        amount = int(serializer.validated_data.get("amount"))
        product_info = product(serializer.validated_data.get("course"),
                               serializer.validated_data.get("lesson"))
        with transaction.atomic():
            """
            Create a Stripe price and session, then save the payment instance.
            If transaction fails, it will roll back.
            """
            price = create_price(amount, product_info)
            session_id, link = create_session(price.id)

            instance = serializer.save(
                user=self.request.user,
                session_id=session_id,
                link=link,
                payment_method="Stripe"
            )


class PaymentUpdateView(UpdateAPIView):
    """
    View to update an existing payment.
    """
    queryset = Payments.objects.all()
    serializer_class = PaymentUpdateSerializer
    permission_classes = [IsAuthenticated, IsUser]

    def perform_update(self, serializer):
        #Update the payment instance with the provided data.

        payment_instance = self.get_object()  # или serializer.instance
        stripe_session_id = payment_instance.session_id
        with transaction.atomic():
            payment_method, payment_status = retrieve_checkout_session(stripe_session_id)
            instance = serializer.save(
                payment_method=payment_method,
                payment_status=payment_status
            )


class PaymentDeleteView(DestroyAPIView):
    """
    View to delete a payment.
    """
    queryset = Payments.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated, IsUser]
