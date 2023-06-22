import json

import requests
from django.contrib import messages
from django.contrib.auth import authenticate
from django.shortcuts import redirect, render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .forms import LoginForm, UserForm
from .models import User
from .serializers import UserSerializer
from .utils import get_refresh_token, send_email

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
        header = "Welcome to Scratch Django!"
        send_email([user.email], header, message)
        return Response({"Success": "User Registered"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"Failed": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def login_user(request):
    user = authenticate(email=request.data["email"], password=request.data["password"])
    if user:
        token = get_refresh_token(user)
        return Response(token, status=status.HTTP_200_OK)
    else:
        return Response({"Failed": "User Not Found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def check_login(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)


# Template Views
def register_user_template(request):
    if request.method == "POST":
        print(request.POST)
        email = request.POST["email"]
        password = request.POST["password"]
        name = request.POST["name"]
        otp_enabled = True if request.POST["otp_enabled"] == ["on"] else False
        url = f"{HOST}/user/register_user/"
        payload = json.dumps(
            {"email": email, "password": password, "name": name, "otp_enabled": otp_enabled}
        )
        headers = {"Content-Type": "application/json"}

        response = requests.request("POST", url, headers=headers, data=payload)
        if response.ok:
            messages.success(request, response.json()["Success"])
            return render(request, "login.html", {"form": LoginForm()})

        else:
            messages.error(request, response.json()["Failed"])
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
            jwt_token = response.json()["access"]
            messages.success(request, "Logged In")
            return redirect("check_login_template", token=jwt_token)

        else:
            messages.error(request, response.json()["Failed"])
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
        print(user)
        return render(request, "display_user.html", {"user": user})
    else:
        return render(request, "failed.html", {"user": user})
