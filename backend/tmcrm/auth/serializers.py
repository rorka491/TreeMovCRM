from django.contrib.auth import get_user_model
from rest_framework import serializers


class RegisterStartSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(min_length=5, max_length=60, required=True)
    password = serializers.CharField(min_length=10, required=True)

    def validate_username(self, username):
        username = username.strip()
        User = get_user_model()

        if " " in username:
            raise serializers.ValidationError("Username must not contain spaces")
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(f'Username: "{username}" is taken')
        return username

    def validate_email(self, email):
        email = email.strip()
        User = get_user_model()

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(f'Email: "{email}" is taken')
        return email


class RegeisterConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    code = serializers.CharField(required=True, max_length=6, min_length=6)
