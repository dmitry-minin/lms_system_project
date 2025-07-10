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
        read_only_fields = ["id", "is_active", "is_staff", "is_superuser"]


class UserShortSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "phone", "city", "avatar"]
        read_only_fields = ["id", "email"]


class UserCreateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password", "phone", "city", "avatar"]
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True, 'error_messages': {'required': 'Email is required.'}},
        }

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

