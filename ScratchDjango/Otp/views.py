import random

from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ScratchDjango.User.models import User
from ScratchDjango.User.utils import get_refresh_token, start_logout_timer

from .constants import GOOGLE_AUTHENTICATOR, QR_HEADER, QR_MESSAGE
from .models import Otp
from .tasks import send_email_qr
from .utils import check_user_otp, generate_otp


@api_view(["POST"])
def create_otp(request):
    data = request.data
    user = User.objects.get(email=data["email"])
    otp = Otp.objects.create(user=user, otp_enabled=data["otp_enabled"])
    if data["otp_enabled"] == GOOGLE_AUTHENTICATOR:
        send_email_qr.delay([user.email], QR_HEADER, QR_MESSAGE.format(user.name), user.id)
    elif data["otp_enabled"] == "Email":
        otp.otp_enabled = "Email"
        otp.save()
    return Response({"message": "Otp Created"}, status=status.HTTP_200_OK)


@api_view(["GET", "POST"])
def check_otp(request):
    email = request.data["email"]
    password = request.data["password"]

    user = authenticate(email=email, password=password)
    if not user:
        return Response({"message": "User Not Found"}, status=status.HTTP_404_NOT_FOUND)

    otp = request.data["otp"]
    val = check_user_otp(user, otp)

    if val:
        token = get_refresh_token(user)
        start_logout_timer(user, token["access"])
        return Response({"token": token}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "Incorrect otp"}, status=status.HTTP_403_FORBIDDEN)
