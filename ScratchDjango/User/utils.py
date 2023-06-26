import re

from django.conf.global_settings import EMAIL_HOST_USER
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from rest_framework_simplejwt.tokens import RefreshToken

from .regex import email_regex


def check_email(email):
    if re.fullmatch(email_regex, email):
        return True
    raise ValidationError("Enter a valid Email")


def send_email(mailto, header, message):
    email = EmailMessage(
        header,
        message,
        EMAIL_HOST_USER,
        mailto,
        reply_to=[EMAIL_HOST_USER],
    )
    email.send(fail_silently=False)


def get_refresh_token(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
