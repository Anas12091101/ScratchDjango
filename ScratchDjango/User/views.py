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

from .forms import LoginForm, ResetEmailForm, ResetForm, UserForm
from .models import User
from .serializers import UserSerializer
from .utils import (
    check_otp_email,
    check_otp_GA,
    generate_email_otp,
    generate_otp,
    get_refresh_token,
    send_email,
)

HOST = "http://127.0.0.1:8000"


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
        if data["otp_enabled"] == "GA":
            otp = generate_otp(user)
            message += f"\n\n You Google Authenticator Key is {otp['base32']}"

        header = "Welcome to Scratch Django!"
        send_email([user.email], header, message)
        return Response({"status": "User Registered."}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"status": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def login_user(request):
    user = authenticate(email=request.data["email"], password=request.data["password"])
    if user:
        if not user.otp_enabled:
            token = get_refresh_token(user)
            return Response({"status": token}, status=status.HTTP_200_OK)
        elif user.otp_enabled == "Email":
            otp = generate_email_otp([user.email])
            user.email_otp = otp
            user.save()
            return Response({"status": "email"}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "GA"}, status=status.HTTP_200_OK)
    else:
        return Response({"status": "User Not Found"}, status=status.HTTP_404_NOT_FOUND)


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
        return Response({"status": "User Not Found"}, status=status.HTTP_404_NOT_FOUND)
    otp = request.data["otp"]
    if user.otp_enabled == "GA": 
        val = check_otp_GA(user, otp)
    elif user.otp_enabled == "Email":
        val = check_otp_email(user, otp)
        if val:
            # Resetting so that it won't be used again
            user.email_otp == "".join([str(random.randint(0, 9)) for i in range(6)])
    else:
        return Response({"status": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)
    if val:
        token = get_refresh_token(user)
        return Response({"status": token}, status=status.HTTP_200_OK)
    else:
        return Response({"status": "Incorrect otp"}, status=status.HTTP_401_UNAUTHORIZED)


# Template Views
def register_user_template(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        name = request.POST["name"]
        otp_enabled = request.POST["otp_enabled"]
        url = f"{HOST}/user/register_user/"
        payload = json.dumps(
            {"email": email, "password": password, "name": name, "otp_enabled": otp_enabled}
        )
        headers = {"Content-Type": "application/json"}

        response = requests.request("POST", url, headers=headers, data=payload)
        if response.ok:
            messages.success(request, response.json()["status"])
            return render(request, "login.html", {"form": LoginForm()})

        else:
            messages.error(request, response.json()["status"])
            return render(request, "register.html", {"form": UserForm()})

    else:
        form = UserForm()
        return render(request, "register.html", {"form": form})


def login_template(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        url = f"{HOST}/user/login/"
        payload = json.dumps({"email": email, "password": password})
        headers = {"Content-Type": "application/json"}

        response = requests.request("POST", url, headers=headers, data=payload)
        if response.ok:
            data = response.json()
            if data["status"] == "GA" or data["status"] == "email":
                return render(request, "otp.html", {"email": email})
            else:
                jwt_token = response.json()["access"]
                messages.success(request, "Logged In")
                return redirect("check_login_template", token=jwt_token)

        else:
            messages.error(request, response.json()["status"])
            return render(request, "login.html", {"form": LoginForm()})

    else:
        form = LoginForm()
        return render(request, "login.html", {"form": form})


def check_login_template(request, token):
    url = f"{HOST}/user/check_login/"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    if response.ok:
        user = response.json()
        return render(request, "display_user.html", {"user": user})
    else:
        return render(request, "failed.html", {"user": user})


def otp_template(request, email):
    if request.method == "POST":
        otp = request.POST["otp"]
        url = f"{HOST}/user/check_otp/"
        headers = {"Content-Type": "application/json"}
        payload = json.dumps({"otp": otp, "email": email})
        response = requests.get(url, headers=headers, data=payload)
        if response.ok:
            jwt_token = response.json()["status"]["access"]
            messages.success(request, "Logged In")
            return redirect("check_login_template", token=jwt_token)
        else:
            messages.error(request, response.json()["status"])
            return render(request, "otp.html", {"email": email})


def reset_template(request):
    if request.method == "POST":
        try:
            email = request.POST["email"]
            url = f"{HOST}/user/api/password_reset/"
            payload = json.dumps({"email": email})
            headers = {"Content-Type": "application/json"}
            response = requests.post(url, headers=headers, data=payload)
            if response.ok:
                messages.success(request, "An email has been forwarded with the reset link")
            else:
                messages.error(request, "Email Not Found")
        except Exception as e:
            messages.error(request, str(e))
        return render(request, "reset.html", {"form": ResetEmailForm()})
    else:
        return render(request, "reset.html", {"form": ResetEmailForm()})


def confirm_reset_template(request, token):
    if request.method == "POST":
        password = request.POST["password"]
        confirm = request.POST["confirm_password"]
        try:
            if password != confirm:
                raise ValidationError("Password donot match")
            url = f"{HOST}/user/api/password_reset/confirm/"
            payload = json.dumps({"token": token, "password": password})
            headers = {"Content-Type": "application/json"}
            response = requests.post(url, headers=headers, data=payload)
            response.raise_for_status()
            if response.ok:
                messages.success(request, "Password Reset Successful")
                return render(request, "login.html", {"form": LoginForm()})
        except Exception as e:
            messages.error(request, str(e))
            return render(request, "reset_password.html", {"form": ResetForm(), "token": token})
    else:
        return render(request, "reset_password.html", {"form": ResetForm(), "token": token})
