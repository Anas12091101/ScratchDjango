from celery import shared_task
from django.conf.global_settings import EMAIL_HOST_USER
from django.core.mail import EmailMessage


@shared_task
def send_email(mailto, header, message):
    email = EmailMessage(
        header,
        message,
        EMAIL_HOST_USER,
        mailto,
        reply_to=[EMAIL_HOST_USER],
    )
    email.send(fail_silently=False)
