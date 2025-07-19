from rest_framework import serializers


class AtLeastOneFieldRequiredValidator:
    def __init__(self, fields, message=None):
        self.fields = fields
        self.message = message or f"Хотя бы одно из полей {fields} должно быть заполнено."

    def __call__(self, attrs):
        if not any(attrs.get(field) for field in self.fields):
            raise serializers.ValidationError(self.message)
        return attrs
