from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.contrib.auth.models import update_last_login
from django.db import IntegrityError, transaction
from django.db.models import Q
from django.core.exceptions import ValidationError as DjangoValidationError
from users.models import User
from users.models import OTP


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)

    default_error_messages = {
        "cannot_create_user": settings.USER_CONSTANTS.messages.CANNOT_CREATE_USER_ERROR
    }

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.LOGIN_FIELD,
            "password",
        )

    def validate_email(self, email):
        try:
            User.objects.get(email=email)
            raise serializers.ValidationError("Email already registered with us")
        except User.DoesNotExist:
            pass
        return email

    def validate(self, attrs):
        user = User(**attrs)
        password = attrs.get("password")
        try:
            validate_password(password, user)
        except DjangoValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {"password": serializer_error["non_field_errors"]}
            )
        return attrs

    def create(self, validated_data):
        try:
            user = self.perform_create(validated_data)
            self.user = user
        except IntegrityError:
            self.fail("cannot_create_user")
        return user

    def perform_create(self, validated_data):
        with transaction.atomic():
            user = User.objects.create_user(**validated_data)
            user.active = False
            user.save(update_fields=["active"])
        return user


class OTPSerializer(serializers.Serializer):
    otp = serializers.IntegerField()

    def validate_otp(self, value):
        try:
            instance = OTP.objects.get(code=value)
            if not instance.is_valid:
                raise serializers.ValidationError(settings.USER_CONSTANTS.messages.INVALID_OTP)
            else:
                self.otp = instance
                return value
        except OTP.DoesNotExist:
                raise serializers.ValidationError(settings.USER_CONSTANTS.messages.OTP_NOT_FOUND)



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "middle_name",
            "last_name",
            "email",
            "identification_type",
            "identification",
            "dob",
            "active",
            "joined_on",
            "updated_on",
        )
