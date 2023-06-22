from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import User


# Create your views here.
@api_view(["POST"])
def register_user(request):
    data = request.data
    try:
        user = User.objects.create_user(password=data["password"], email=data["email"])
        return Response({"Success": "User Registered"})
    except Exception as e:
        return Response({"Failed": str(e)})
