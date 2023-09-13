from celery import shared_task
from django.conf.global_settings import EMAIL_HOST_USER
from django.core.mail import EmailMultiAlternatives

from ScratchDjango.User.models import User

from .utils import create_qr_data, generate_otp


@shared_task
def send_email_qr(mailto, header, message, user_id):
    user = User.objects.get(id=user_id)
    qrcode = generate_otp(user)["qrcode"]
    email = EmailMultiAlternatives(
        header,
        message,
        EMAIL_HOST_USER,
        mailto,
        reply_to=[EMAIL_HOST_USER],
    )
    email.mixed_subtype = "related"
    email.attach(create_qr_data(qrcode))
    email.send(fail_silently=False)
