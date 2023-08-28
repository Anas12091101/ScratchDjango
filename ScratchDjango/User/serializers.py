from rest_framework import serializers

from .models import User
from .validators import check_email

# from ScratchDjango.Profile.serializers import ProfileSerializer



class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[check_email])
    class Meta:
        model = User
        fields = ("id", "name", "email", "password")
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
        