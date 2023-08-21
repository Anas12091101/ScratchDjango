from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ScratchDjango.User.models import User
from ScratchDjango.User.serializers import UserSerializer

from .models import Profile
from .serializers import ProfileSerializer


# Create your views here.
@api_view(["POST","PUT"])
@permission_classes([IsAuthenticated])
def create_or_update(request):
    try:
        user_email = request.user.email
        if request.method == "POST":
            profile_serializer = ProfileSerializer(data=request.data, context={"email":user_email}, partial=True)
            message = "Profile Created"
        else:
            profile = Profile.objects.get(user=request.user)
            profile_serializer = ProfileSerializer(profile,data=request.data, context={"email":user_email}, partial=True)
            message = "Profile Updated"
        if profile_serializer.is_valid():
            profile_serializer.save()
        else:
            raise ValidationError(profile_serializer.errors)
        return Response({"message":message})
    except ValidationError as e:
        return Response({"message": e}, status=status.HTTP_400_BAD_REQUEST)
