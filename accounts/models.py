from uuid import uuid4
from django.db import models
from users.models import User


class Account(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    account_id = models.BigIntegerField(unique=True)
    user = models.OneToOneField(
        User, related_name="account", on_delete=models.CASCADE)
    currency = models.CharField(max_length=4, blank=True, null=True)
    balance = models.FloatField()
    description = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.user.get_full_name()


class AccountActivity(models.Model):
    PUSH = 'PULL'
    PULL = 'PUSH'
    RECEIVE = "RECEIVE"
    ACTIVITY_TYPE_CHOICES = (
        (PUSH, "Push"),
        (PULL, "Pull"),
        (RECEIVE, "Receive"),
    )
    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    account = models.ForeignKey(
        Account, related_name="activities", on_delete=models.CASCADE)
    current_balance = models.FloatField()
    balance = models.FloatField()
    activity_type = models.CharField(
        choices=ACTIVITY_TYPE_CHOICES,max_length=10, default=PUSH)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.account



