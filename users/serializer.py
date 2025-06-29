from rest_framework.serializers import ModelSerializer
from users.models import User, Payments


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payments
        fields = ["id", "user", "payment_date", "course", "lesson", "amount", "payment_method"]
        read_only_fields = ["id", "payment_date"]


class UserSerializer(ModelSerializer):
    payments_history = PaymentSerializer(many=True, read_only=True, source="payments")

    class Meta:
        model = User
        fields = ["id", "email", "phone", "city", "avatar", "is_active", "is_staff", "is_superuser", "payments_history"]
