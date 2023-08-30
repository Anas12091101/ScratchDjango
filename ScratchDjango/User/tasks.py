from celery import shared_task
from django.conf.global_settings import EMAIL_HOST_USER
from django.core.cache import cache
from django.core.mail import EmailMessage

from .models import User


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


@shared_task
def perform_logout(user_id, token):
    user = User.objects.get(id=user_id)
    cache.set(token, "expired", timeout=24 * 60 * 60)
    user.logout_task_id = "NA"
    user.save()
