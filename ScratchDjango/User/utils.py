import random
from email.mime.image import MIMEImage
from io import BytesIO

import jwt
import pyotp
import qrcode
from django.conf import settings
from django.conf.global_settings import EMAIL_HOST_USER
from django.core.mail import EmailMessage, EmailMultiAlternatives
from rest_framework_simplejwt.tokens import RefreshToken

from .constants import GOOGLE_AUTHENTICATOR
from .tasks import send_email


def get_refresh_token(user):
    refresh = RefreshToken.for_user(user)
    payload = jwt.decode(str(refresh.access_token), settings.SECRET_KEY , algorithms=["HS256"])
    print(user.id)
    user.last_token_iat = payload['iat']
    user.save()
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }

def generate_otp(user):
    otp_base32 = pyotp.random_base32()
    otp_auth_url = pyotp.totp.TOTP(otp_base32).provisioning_uri(
        name=user.email.lower(), issuer_name="scratchdjango"
    )

    img = qrcode.make(otp_auth_url)
    user.otp.otp_enabled = GOOGLE_AUTHENTICATOR
    user.otp.otp_auth_url = otp_auth_url
    user.otp.otp_base32 = otp_base32
    user.otp.save()

    return {"base32": otp_base32, "otpauth_url": otp_auth_url, "qrcode":img}

def generate_email_otp(email):
    otp = ""
    for i in range(6):
        otp += str(random.randint(0, 9))
    send_email.delay(email, "OTP", f"Your OTP is {otp}")
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
