from django.core.cache import cache
from django.dispatch import receiver, Signal
from django.db.models.signals import post_save,post_delete
from users.models import User
from core.models import Transaction
transaction_created = Signal


@receiver(post_save,Transaction)
def set_transaction_cache(sender, instance,created, **kwargs):
    user = instance.sender
    transactions = list(Transaction.objects.filter(sender=user))
    cache.set(f'{user.email}-transactions', transactions, 604800)

@receiver(post_delete,Transaction)
def clear_transactions(sender,instance,**kwargs):
    user = instance.sender
    cache_key = f"{user.email}-transactions"
    if cache.get(cache_key):
        cache.delete(cache_key)
        transactions = list(Transaction.objects.filter(sender=user))
        cache.set(cache_key, transactions, 604800)

