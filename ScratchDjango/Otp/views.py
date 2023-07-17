import random

from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ScratchDjango.User.models import User

from .constants import GOOGLE_AUTHENTICATOR, QR_HEADER
from .models import Otp
from .utils import (
    check_otp_email,
    check_otp_GA,
    generate_otp,
    get_refresh_token,
    send_email_qr,
)


@api_view(["POST"])
def create_otp(request):
    data = request.data
    user = User.objects.get(email = data["email"])
    otp = Otp.objects.create(user = user, otp_enabled = data["otp_enabled"])
    QR_MESSAGE = f"Hi {user.name} , Kindly find the attached QR Code for Google Authenticator"
    if data["otp_enabled"] == GOOGLE_AUTHENTICATOR:
        otp = generate_otp(user)
        send_email_qr([user.email], QR_HEADER, QR_MESSAGE, qrcode=otp["qrcode"])
    elif data["otp_enabled"] == "Email":
            otp.otp_enabled = "Email"
            otp.save()
    return Response({"message": "Otp Created"}, status=status.HTTP_200_OK)

@api_view(["GET","POST"])
def check_otp(request):
    email = request.data["email"]
    password = request.data["password"]
    user = authenticate(email=email, password=password)
    if not user:
        return Response({"message": "User Not Found"}, status=status.HTTP_404_NOT_FOUND)
    otp = request.data["otp"]
    if user.otp.otp_enabled == GOOGLE_AUTHENTICATOR: 
        val = check_otp_GA(user, otp)
    elif user.otp.otp_enabled == "Email":
        val = check_otp_email(user, otp)
        if val:
            # Resetting so that it won't be used again
            user.otp.email_otp == "".join([str(random.randint(0, 9)) for i in range(6)])
    else:
        return Response({"message": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)
    if val:
        token = get_refresh_token(user)
        return Response({"token": token}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "Incorrect otp"}, status=status.HTTP_401_UNAUTHORIZED)


