from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework import serializers

from ScratchDjango.User.models import User
from ScratchDjango.User.serializers import UserSerializer

from .models import Profile
from .validators import validate_image


@receiver(post_save, sender=User)
def create_profile(sender, instance, **kwargs):
    profile_serializer = ProfileSerializer(data={}, context={"email":instance.email}, partial=True)
    if profile_serializer.is_valid():
        profile_serializer.save()

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