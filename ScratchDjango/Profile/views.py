from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Profile
from .serializers import ProfileSerializer


# Profile will automatically be created when the user is registered.
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user_email = request.user.email
    profile = Profile.objects.get(user=request.user)
    profile_serializer = ProfileSerializer(
        profile, data=request.data, context={"email": user_email}, partial=True
    )
    message = "Profile Updated"
    if profile_serializer.is_valid():
        profile_serializer.save()
        return Response({"message": message})
    else:
        raise Response({"message": profile_serializer.errors})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    profile = Profile.objects.get(user=request.user)
    serializer = ProfileSerializer(profile, many=False)
    return Response(serializer.data)


@api_view(["GET"])
def get_all_profile(request):
    profile = Profile.objects.all()
    serializer = ProfileSerializer(profile, many=True)
    return Response(serializer.data)
