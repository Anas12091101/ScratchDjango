from django.contrib.auth import authenticate
from django.core.cache import cache
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from ScratchDjango.Otp.utils import generate_email_otp

from .constants import GOOGLE_AUTHENTICATOR, WELCOME_HEADER
from .models import User
from .serializers import UserSerializer
from .tasks import send_email
from .utils import get_refresh_token, start_logout_timer


# API Views
@api_view(["POST"])
def register_user(request):
    email = request.data["email"]
    user_serializer = UserSerializer(data=request.data)
    if user_serializer.is_valid():
        user_serializer.save()
        message = f"Hi {email}, Welcome to DjangoFromScratch. We hope you enjoy our product and have a good time here."
        send_email.delay([email], WELCOME_HEADER, message)
        return Response({"message": "User Registered."}, status=status.HTTP_200_OK)
    else:
        return Response({"message": user_serializer.errors})


@api_view(["POST"])
def login_user(request):
    user = authenticate(email=request.data["email"], password=request.data["password"])
    if user:
        if not user.otp.otp_enabled:
            token = get_refresh_token(user)
            start_logout_timer(user, token["access"])
            return Response({"token": token}, status=status.HTTP_200_OK)

        # If email otp is enabled, we need to generate an email_otp here and save it.
        elif user.otp.otp_enabled == "Email":
            otp = generate_email_otp([user.email])
            user.otp.email_otp = otp
            user.otp.save()
            user.save()
            return Response({"type": "email"}, status=status.HTTP_200_OK)

        else:
            return Response({"type": GOOGLE_AUTHENTICATOR}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "User Not Found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
@permission_classes([IsAdminUser])
def blacklist_token(request):
    token = request.data["token"]
    cache.set(token, "expired", timeout=24 * 60 * 60)  # setting for max 24 hrs
    return Response({"message": "Updated blacklist"})
