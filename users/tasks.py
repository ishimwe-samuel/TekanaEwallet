from celery import shared_task
from users.models import OTP, User
from utils.code_generator import CodeGenerator
from accounts.models import Account
from core.tasks import email_notifier


@shared_task
def account_setup(user_id):
    user = User.objects.get(pk=user_id)
    account_id = CodeGenerator.generate_account_number()
    code = CodeGenerator.generate_otp(digit=True)
    while OTP.objects.filter(code=code).exists():
        code = CodeGenerator.generate_otp(digit=True)
    instance = OTP.objects.create(
        user=user, code=code, otp_type=OTP.REGISTRATION)
    email_notifier.delay("Welcome to Tekana e-Wallet",
               message=f"Hello {user.get_full_name()} \nPlease use this code to verify your account | {instance.code}",to=user.email)
    while Account.objects.filter(account_id=account_id).exists():
        account_id = CodeGenerator.generate_account_number()
    Account.objects.create(user=user,balance=10000,account_id=account_id)