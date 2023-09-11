import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .serializers import MessageSerializer


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
        message = text_data_json["message"]
        data = {"message": message, "room": self.room_name}

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

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]
        profile = event["profile"]
        data = {"message": message, "room": self.room_name, "profile": profile}
        self.send(text_data=json.dumps(data))

    def create_message(self, message):
        message_serializer = MessageSerializer(
            data=message, context={"email": self.scope["user"].email}, partial=True
        )
        if message_serializer.is_valid():
            message_serializer.save()
        else:
            print(message_serializer.errors)
