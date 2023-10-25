from uuid import uuid4
from django.db import models
from users.models import User
from .validators import null_validator, expiration_date_validator


class PaymentCards(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(User, related_name="cards",
                             on_delete=models.CASCADE)
    cvv = models.IntegerField()
    balance = models.FloatField()
    expiration_date = models.CharField(max_length=5, validators=[
                                       expiration_date_validator])
    is_active = models.BooleanField(default=True)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"

    def __str__(self):
        return self.name


class Transaction(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    sender = models.ForeignKey(
        User, related_name="sent_transactions", null=True, on_delete=models.SET_NULL, validators=[null_validator])
    receiver = models.ForeignKey(
        User, related_name="received_transactions", null=True, on_delete=models.SET_NULL, validators=[null_validator])
    amount = models.FloatField()
    description = models.TextField()
    transanction_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"

    def __str__(self):
        return self.sender.get_full_name()


class Currency(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    currency_name = models.CharField(max_length=50)
    currency_symbol = models.CharField(max_length=5)

    class Meta:
        verbose_name = "Currency"
        verbose_name_plural = "Currencies"

    def __str__(self):
        return self.currency_name


class CurrencyExchangeRate(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    base_currency = models.ForeignKey(Currency,related_name="base_currencies", on_delete=models.CASCADE)
    target_currency = models.ForeignKey(Currency,related_name="target_currency", on_delete=models.CASCADE)
    rate = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, related_name="currency_created", on_delete=models.SET_NULL, null=True, validators=[null_validator])
    updated_by = models.ForeignKey(
        User, related_name="currency_updates", on_delete=models.SET_NULL, null=True, validators=[null_validator])

    class Meta:
        verbose_name = "Currency Exchange Rate"
        verbose_name_plural = "Currency Exchange Rates"

    def __str__(self):
        return self.base_currency
