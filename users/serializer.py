from rest_framework.serializers import ModelSerializer
from users.models import User, Payments
from users.validators import AtLeastOneFieldRequiredValidator


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payments
        fields = ["id", "user", "payment_date", "course", "lesson", "amount", "payment_method", "session_id", "link",
                  "payment_status"]
        read_only_fields = ["id", "user", "payment_date", "payment_method", "payment_status", "session_id", "link"]
        validators = [AtLeastOneFieldRequiredValidator(fields=["course", "lesson"])]


class PaymentUpdateSerializer(ModelSerializer):
    class Meta:
        model = Payments
        fields = ["id", "user", "payment_date", "course", "lesson", "amount", "payment_method", "payment_status",
                  "session_id", "link"]
        read_only_fields = ["user", "payment_date", "course", "lesson", "amount", "payment_method", "payment_status",
                            "session_id","link"]


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
