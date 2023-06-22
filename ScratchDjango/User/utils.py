<<<<<<< HEAD
<<<<<<< HEAD
import random
from email.mime.image import MIMEImage
from io import BytesIO
=======
=======
import random

import pyotp
>>>>>>> e021e6b (Email OTP + Google Authenticator OTP Login)
from django.conf.global_settings import EMAIL_HOST_USER
from django.core.mail import EmailMessage
from rest_framework_simplejwt.tokens import RefreshToken
>>>>>>> 29ca7a9 (Implemented JWT Login)

import jwt
import pyotp
import qrcode
from django.conf import settings
from django.conf.global_settings import EMAIL_HOST_USER
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage, EmailMultiAlternatives
from rest_framework_simplejwt.tokens import RefreshToken

from ScratchDjango.Otp.models import Otp

from .constants import GOOGLE_AUTHENTICATOR


def create_qr_data(qrcode):
    buffer = BytesIO()
    qrcode.save(buffer)
    buffer.seek(0)
    binary_data = buffer.getvalue()
    image = MIMEImage(binary_data)
    return image

def send_email_qr(mailto, header, message, qrcode):
    email = EmailMultiAlternatives(
        header,
        message,
        EMAIL_HOST_USER,
        mailto,
        reply_to=[EMAIL_HOST_USER],
    )
    email.mixed_subtype = 'related'
    email.attach(create_qr_data(qrcode))
    email.send(fail_silently=False)

def send_email(mailto, header, message):
    email = EmailMessage(
        header,
        message,
        EMAIL_HOST_USER,
        mailto,
        reply_to=[EMAIL_HOST_USER],
    )
    email.send(fail_silently=False)

<<<<<<< HEAD
def get_refresh_token(user):
    refresh = RefreshToken.for_user(user)
    payload = jwt.decode(str(refresh.access_token), settings.SECRET_KEY , algorithms=["HS256"])
    print(user.id)
    user.last_token_iat = payload['iat']
    user.save()
=======

def get_refresh_token(user):
    refresh = RefreshToken.for_user(user)

>>>>>>> 29ca7a9 (Implemented JWT Login)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> e021e6b (Email OTP + Google Authenticator OTP Login)


def generate_otp(user):
    otp_base32 = pyotp.random_base32()
    otp_auth_url = pyotp.totp.TOTP(otp_base32).provisioning_uri(
        name=user.email.lower(), issuer_name="scratchdjango"
    )

<<<<<<< HEAD
    img = qrcode.make(otp_auth_url)
    user.otp.otp_enabled = GOOGLE_AUTHENTICATOR
    user.otp.otp_auth_url = otp_auth_url
    user.otp.otp_base32 = otp_base32
    user.otp.save()

    return {"base32": otp_base32, "otpauth_url": otp_auth_url, "qrcode":img}
=======
    user.otp_auth_url = otp_auth_url
    user.otp_base32 = otp_base32
    user.save()

    return {"base32": otp_base32, "otpauth_url": otp_auth_url}

>>>>>>> e021e6b (Email OTP + Google Authenticator OTP Login)

def generate_email_otp(email):
    otp = ""
    for i in range(6):
        otp += str(random.randint(0, 9))
    send_email(email, "OTP", f"Your OTP is {otp}")
    return otp


def check_otp_GA(user, otp):
<<<<<<< HEAD
    totp = pyotp.TOTP(user.otp.otp_base32)
=======
    totp = pyotp.TOTP(user.otp_base32)
>>>>>>> e021e6b (Email OTP + Google Authenticator OTP Login)
    if not totp.verify(otp):
        return False
    return True


def check_otp_email(user, otp):
<<<<<<< HEAD
    if user.otp.email_otp == otp:
        return True
    return False
=======
>>>>>>> 29ca7a9 (Implemented JWT Login)
=======
    if user.email_otp == otp:
        return True
    return False
>>>>>>> e021e6b (Email OTP + Google Authenticator OTP Login)
