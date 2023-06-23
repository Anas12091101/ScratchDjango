import json

import requests
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .constants import HOST
from .forms import UserForm
from .models import User


# API Views
@api_view(["POST"])
def register_user(request):
    data = request.data
    try:
        user = User.objects.create_user(password=data["password"], email=data["email"])
        return Response({"Success": "User Registered"}, status=status.HTTP_200_OK)
    except ValidationError as e:
        return Response({"Failed": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# Template Views
def register_user_template(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        url = f"{HOST}/user/register_user/"
        payload = json.dumps({"email": email, "password": password})
        headers = {"Content-Type": "application/json"}

        response = requests.request("POST", url, headers=headers, data=payload)
        if response.ok:
            messages.success(request, response.json()["Success"])
        else:
            messages.error(request, response.json()["Failed"])
        return render(request, "register.html", {"form": UserForm()})

    else:
        form = UserForm()
        return render(request, "register.html", {"form": form})
