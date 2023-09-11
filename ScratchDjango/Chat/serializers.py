from rest_framework import serializers

from ScratchDjango.Profile.models import Profile
from ScratchDjango.Profile.serializers import ProfileSerializer
from ScratchDjango.User.models import User

from .models import Message


class MessageSerializer(serializers.Serializer):
    message = serializers.CharField()
    room = serializers.CharField()
    profile = ProfileSerializer()

    def create(self, validated_data):
        user = User.objects.get(email=self.context["email"])
        profile = Profile.objects.get(user=user)
        return Message.objects.create(profile=profile, **validated_data)

    def update(self, instance, validated_data):
        instance.message = validated_data.get("message", instance.message)
        instance.room = validated_data.get("room", instance.room)
        instance.save()
        return instance
