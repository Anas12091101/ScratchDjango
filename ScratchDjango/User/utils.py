from django.conf.global_settings import EMAIL_HOST_USER
from django.core.mail import EmailMessage
from rest_framework_simplejwt.tokens import RefreshToken


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
