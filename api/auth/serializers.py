from django.conf import settings
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class JWTTokenSerializer(TokenObtainPairSerializer):
    """This Serializer handles login details"""
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token

    def validate(self, attrs):
        self.request = self.context.get('request')
        data = super().validate(attrs)
        if self.user.is_suspended:
            raise serializers.ValidationError(
                settings.ACCOUNT_CONSTANTS.messages.SUSPENDED_ACCOUNT)
        if not self.user.active:
            raise serializers.ValidationError(
                settings.ACCOUNT_CONSTANTS.messages.INACTIVE_ACCOUNT_ERROR)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        update_last_login(None, self.user)
        return data
