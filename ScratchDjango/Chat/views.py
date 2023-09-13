from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import FileMessage, Message
from .serializers import FileMessageSerializer, MessageSerializer


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


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def upload_file(request):
    user = request.user
    types = dict(request.POST)["types[]"]
    files = dict(request.FILES)["files[]"]
    errors = []
    ids = []
    for idx, file in enumerate(list(files)):
        ser = FileMessageSerializer(
            data={"file_url": file, "file_type": types[idx]}, context={"id": user.id}, partial=True
        )
        if ser.is_valid():
            new_file = ser.save()
            ids.append(new_file.id)
        else:
            print(ser.errors)
            errors += ser.errors["file_url"]
        # new_file = FileMessage.objects.create(user=user, file_url=file, file_type=types[idx])
    if errors:
        return Response({"message": errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    # file = FileMessage.objects.create(user=user, file_url=file, file_type=file_type)
    return Response({"ids": ids})
