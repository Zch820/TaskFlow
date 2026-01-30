from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from apps.common.sanitizers import sanitize_plain_text
from apps.users.models import User


class UserRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

    def validate_email(self, email):
        email = email.lower().strip()
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already registered")
        return email

    def validate_first_name(self, value):
        return sanitize_plain_text(value)

    def validate_last_name(self, value):
        return sanitize_plain_text(value)

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords don't match")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')
        new_user = User(**validated_data)
        new_user.set_password(password)
        new_user.save()
        return new_user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email')
