from django.core.cache import cache
from rest_framework import status, mixins, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from accounts.models import Account, AccountActivity
from core.models import Transaction
from api.v1.accounts.permissions import IsAccountOwmer
from api.v1.accounts.serializers import (
    AccountSerializer, AccountActivitySerializer, TransferFundsSerializer, TransactionSerializer)


class AccountsViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAccountOwmer]

    def get_serializer_class(self):
        if self.action == "get_account_activity":
            return AccountActivitySerializer
        if self.action == "":
            return TransferFundsSerializer
        if self.action == "get_account":
            return AccountSerializer
        if self.action == "transfer_funds":
            return TransferFundsSerializer
        if self.action == "get_transactions":
            return TransactionSerializer
        return super().get_serializer_class()

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['request'] = self.request
        return ctx

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user.account)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(method="GET", operation_id='Account Activity', responses={200: AccountActivitySerializer(many=True)})
    @action(["GET"], detail=False, url_path='activity')
    def get_account_activity(self, request, *args, **kwargs):
        "Get a user related activities"
        instance = request.user.account
        activity_instances = AccountActivity.objects.filter(account=instance)
        serializer = self.get_serializer(activity_instances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(method="POST", request_body=TransferFundsSerializer, operation_id='Transfer Funds', responses={200: TransferFundsSerializer})
    @action(["POST"], detail=False, url_path='transact')
    def transfer_funds(self, request, *args, **kwargs):
        """
        Allows the user to transfer funds to another user 
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(method="GET", operation_id='User Account Transactions', responses={200: TransactionSerializer(many=True)})
    @action(["GET"], detail=False, url_path='transactions')
    def get_transactions(self, request, *args, **kwargs):
        """
        Allows the user to view his account transactions
        """
        transactions = []
        cached_transactions = cache.get(f'{request.user.email}-transactions')
        if cached_transactions:
            transactions = cached_transactions
        else:
            transactions = Transaction.objects.filter(sender=request.user)
        serializer = self.get_serializer(transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
