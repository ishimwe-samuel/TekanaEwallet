from django.core.mail import send_mail 
from django.conf import settings
from celery import shared_task


@shared_task
def email_notifier(subject, message, to):
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [to],
        fail_silently=False,
    )
