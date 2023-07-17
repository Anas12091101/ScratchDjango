from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ScratchDjango.Otp.utils import generate_email_otp

from .constants import GOOGLE_AUTHENTICATOR, WELCOME_HEADER
from .models import User
from .serializers import UserSerializer
from .utils import get_refresh_token, send_email


# API Views
@api_view(["POST"])
def register_user(request):
    data = request.data
    try:
        user = User.objects.create_user(
            name=data["name"],
            password=data["password"],
            email=data["email"],
        )
        message = f"Hi {user.email}, Welcome to DjangoFromScratch. We hope you enjoy our product and have a good time here."
        send_email([user.email], WELCOME_HEADER, message)
        return Response({"message": "User Registered."}, status=status.HTTP_200_OK)
    except ValidationError as e:
        return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def login_user(request):
    user = authenticate(email=request.data["email"], password=request.data["password"])
    if user:
        if not user.otp.otp_enabled:
            token = get_refresh_token(user)
            return Response({"token": token}, status=status.HTTP_200_OK)
        elif user.otp.otp_enabled == "Email":
            otp = generate_email_otp([user.email])
            user.otp.email_otp = otp
            user.otp.save()
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
