import random
from email.mime.image import MIMEImage
from io import BytesIO

import pyotp
import qrcode
from django.conf import settings
from django.conf.global_settings import EMAIL_HOST_USER
from django.core.mail import EmailMessage, EmailMultiAlternatives
from rest_framework_simplejwt.tokens import RefreshToken

from .constants import GOOGLE_AUTHENTICATOR


def create_qr_data(qrcode):
    buffer = BytesIO()
    qrcode.save(buffer)
    buffer.seek(0)
    binary_data = buffer.getvalue()
    image = MIMEImage(binary_data)
    return image


def send_email(mailto, header, message):
    email = EmailMessage(
        header,
        message,
        EMAIL_HOST_USER,
        mailto,
        reply_to=[EMAIL_HOST_USER],
    )
    email.send(fail_silently=False)


def generate_otp(user):
    otp_base32 = pyotp.random_base32()
    otp_auth_url = pyotp.totp.TOTP(otp_base32).provisioning_uri(
        name=user.email.lower(), issuer_name=settings.OTP_ISSUER_NAME
    )

    img = qrcode.make(otp_auth_url)
    user.otp.otp_enabled = GOOGLE_AUTHENTICATOR
    user.otp.otp_auth_url = otp_auth_url
    user.otp.otp_base32 = otp_base32
    user.otp.save()

    return {"base32": otp_base32, "otpauth_url": otp_auth_url, "qrcode": img}


def generate_email_otp(email):
    otp = ""
    for i in range(6):
        otp += str(random.randint(0, 9))
    send_email(email, "OTP", f"Your OTP is {otp}")
    return otp


def check_otp_GA(user, otp):
    totp = pyotp.TOTP(user.otp.otp_base32)
    if not totp.verify(otp):
        return False
    return True


def check_otp_email(user, otp):
    if user.otp.email_otp == otp:
        return True
    return False


def check_user_otp(user, otp):
    if user.otp.otp_enabled == GOOGLE_AUTHENTICATOR:
        val = check_otp_GA(user, otp)
    elif user.otp.otp_enabled == "Email":
        val = check_otp_email(user, otp)
        if val:
            # Resetting so that it won't be used again
            user.otp.email_otp == "".join([str(random.randint(0, 9)) for i in range(6)])
            user.otp.save()
            user.save()
    return val
