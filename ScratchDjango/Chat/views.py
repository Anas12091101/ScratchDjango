from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Message
from .serializers import MessageSerializer


# Validating room and sending room's previous messages in response
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def validate_room(request):
    room = request.data["room"]
    user = request.user
    if str(user.id) not in room.split("_"):
        return Response(
            {"message": "You cannot enter this room"}, status=status.HTTP_403_FORBIDDEN
        )
    messages = Message.objects.filter(room=room)
    serializer = MessageSerializer(messages, many=True)
    return Response({"messages": serializer.data}, status=status.HTTP_200_OK)
