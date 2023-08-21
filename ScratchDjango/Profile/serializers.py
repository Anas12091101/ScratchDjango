from rest_framework import serializers

from ScratchDjango.User.models import User
from ScratchDjango.User.serializers import UserSerializer

from .models import Profile
from .validators import validate_image


class ProfileSerializer(serializers.Serializer):
    user = UserSerializer()
    avatar = serializers.ImageField(validators=[validate_image])
    bio = serializers.CharField()
    
    def create(self, validated_data):
        user = User.objects.get(email = self.context["email"])
        return Profile.objects.create(user=user,**validated_data)

    def update(self, instance, validated_data):
        instance.avatar = validated_data.get("avatar", instance.avatar)
        instance.bio = validated_data.get("bio", instance.bio)
        instance.save()
        return instance