import json
import random

import requests
from django.contrib import messages
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .constants import GOOGLE_AUTHENTICATOR, HOST, WELCOME_HEADER
from .models import User
from .serializers import UserSerializer
from .utils import (
    check_otp_email,
    check_otp_GA,
    generate_email_otp,
    generate_otp,
    get_refresh_token,
    send_email,
    send_email_qr,
)


# API Views
@api_view(["POST"])
def register_user(request):
    data = request.data
    try:
        user = User.objects.create_user(
            name=data["name"],
            otp_enabled=data["otp_enabled"],
            password=data["password"],
            email=data["email"],
        )

        message = f"Hi {user.email}, Welcome to DjangoFromScratch. We hope you enjoy our product and have a good time here."
        if data["otp_enabled"] == GOOGLE_AUTHENTICATOR:
            otp = generate_otp(user)
            send_email_qr([user.email], WELCOME_HEADER, message, qrcode=otp["qrcode"])
        else:
            send_email([user.email], WELCOME_HEADER, message)
        return Response({"message": "User Registered."}, status=status.HTTP_200_OK)
    except ValidationError as e:
        return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def login_user(request):
    user = authenticate(email=request.data["email"], password=request.data["password"])
    if user:
        if not user.otp_enabled:
            token = get_refresh_token(user)
            return Response({"token": token}, status=status.HTTP_200_OK)
        elif user.otp_enabled == "Email":
            otp = generate_email_otp([user.email])
            user.email_otp = otp
            user.save()
            return Response({"type": "email"}, status=status.HTTP_200_OK)
        else:
            return Response({"type": GOOGLE_AUTHENTICATOR},status=status.HTTP_200_OK)
    else:
        return Response({"message": "User Not Found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def check_login(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)


@api_view(["GET","POST"])
def check_otp(request):
    email = request.data["email"]
    password = request.data["password"]
    user = authenticate(email=email, password=password)
    if not user:
        return Response({"message": "User Not Found"}, status=status.HTTP_404_NOT_FOUND)
    otp = request.data["otp"]
    if user.otp_enabled == "GA": 
        val = check_otp_GA(user, otp)
    elif user.otp_enabled == "Email":
        val = check_otp_email(user, otp)
        if val:
            # Resetting so that it won't be used again
            user.email_otp == "".join([str(random.randint(0, 9)) for i in range(6)])
    else:
        return Response({"message": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)
    if val:
        token = get_refresh_token(user)
        return Response({"token": token}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "Incorrect otp"}, status=status.HTTP_401_UNAUTHORIZED)
