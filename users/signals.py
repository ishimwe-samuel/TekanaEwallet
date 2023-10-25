from django.dispatch import Signal, receiver
from users.tasks import account_setup
user_account_created = Signal()


@receiver(user_account_created)
def account_created(sender,user, **kwargs):
    # create an account with a bonus of 10,000 funds
    account_setup(user_id=user.id)
    pass
