import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .models import FileMessage
from .serializers import FileMessageSerializer, MessageSerializer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        # Join room group
        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)

        # handling text messages
        if text_data_json["type"] == "text":
            message = text_data_json["message"]
            data = {"message": message, "room": self.room_name, "type": "text"}
            profile = text_data_json["profile"]
            if profile["user"]["email"] == self.scope["user"].email:
                message_serializer = MessageSerializer(
                    data=data, context={"email": self.scope["user"].email}, partial=True
                )
                if message_serializer.is_valid():
                    message_serializer.save()
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {"type": "chat.message", "message": message, "profile": profile},
            )

        # handling file messages
        else:
            id = text_data_json["message"]
            filemsg = FileMessage.objects.get(id=id)
            profile = text_data_json["profile"]
            url = FileMessageSerializer(filemsg).data["file_url"]
            data = {"message": url, "room": self.room_name, "type": filemsg.file_type}
            if profile["user"]["email"] == self.scope["user"].email:
                message_serializer = MessageSerializer(
                    data=data, context={"email": self.scope["user"].email}, partial=True
                )
                if message_serializer.is_valid():
                    message_serializer.save()
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    "type": "chat.file",
                    "message": url,
                    "profile": profile,
                    "file_type": filemsg.file_type,
                },
            )

    # Receive file message from room group
    def chat_file(self, event):
        message = event["message"]
        profile = event["profile"]
        file_type = event["file_type"]
        data = {"message": message, "room": self.room_name, "profile": profile, "type": file_type}
        self.send(text_data=json.dumps(data))

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]
        profile = event["profile"]
        data = {"message": message, "room": self.room_name, "profile": profile, "type": "text"}
        self.send(text_data=json.dumps(data))

    def create_message(self, message):
        message_serializer = MessageSerializer(
            data=message, context={"email": self.scope["user"].email}, partial=True
        )
        if message_serializer.is_valid():
            message_serializer.save()
        else:
            print(message_serializer.errors)
