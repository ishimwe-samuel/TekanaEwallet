from django.conf import settings
from rest_framework import serializers
from accounts.models import Account, AccountActivity
from core.models import Transaction
from core.models import Transaction
from users.models import User
from api.v1.users.serializers import UserSerializer
from core.validators import null_validator


class AccountSerializer(serializers.ModelSerializer):
    """
    A detailed serializer for account 
    """
    class Meta:
        model = Account
        fields = '__all__'


class AccountActivitySerializer(serializers.ModelSerializer):
    """
    A list serializer for account activity
    """
    class Meta:
        model = AccountActivity
        fields = '__all__'


class TransferFundsSerializer(serializers.ModelSerializer):
    """
    This serializer performs a transaction to both the sender and receiver accounts
    """
    sender = serializers.ReadOnlyField(default=serializers.CurrentUserDefault())
    receiver = serializers.PrimaryKeyRelatedField(
        allow_null=True, queryset=User.objects.all(), required=True, validators=[null_validator])

    class Meta:
        model = Transaction
        fields = '__all__'

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        sender = validated_data.get('sender')
        sender_account = sender.account
        amount = validated_data.get('amount')
        if sender_account.balance < amount:
            raise serializers.ValidationError(
                {'amount': settings.ACCOUNT_CONSTANTS.messages.INSUFFICIENT_FUNDS})
        return validated_data

    def create(self, validated_data):
        sender = validated_data.get('sender')
        receiver = validated_data.get('receiver')
        sender_account = sender.account
        receiver_account = receiver.account
        amount = validated_data.get('amount')
        sender_account.balance -= amount
        receiver_account.balance += amount
        sender_account.save()
        receiver_account.save()
        return super().create(validated_data)
    
class TransactionSerializer(TransferFundsSerializer):
    "This is a transaction serializer that helps "
    receiver = serializers.SerializerMethodField()

    def get_receiver(self,obj):
        return UserSerializer(obj.receiver).data