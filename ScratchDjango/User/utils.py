import random
import re

import pyotp
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


def generate_otp(user):
    otp_base32 = pyotp.random_base32()
    otp_auth_url = pyotp.totp.TOTP(otp_base32).provisioning_uri(
        name=user.email.lower(), issuer_name="scratchdjango"
    )

    user.otp_auth_url = otp_auth_url
    user.otp_base32 = otp_base32
    user.save()

    return {"base32": otp_base32, "otpauth_url": otp_auth_url}


def generate_email_otp(email):
    otp = ""
    for i in range(6):
        otp += str(random.randint(0, 9))
    send_email(email, "OTP", f"Your OTP is {otp}")
    return otp


def check_otp_GA(user, otp):
    totp = pyotp.TOTP(user.otp_base32)
    if not totp.verify(otp):
        return False
    return True


def check_otp_email(user, otp):
    if user.email_otp == otp:
        return True
    return False
