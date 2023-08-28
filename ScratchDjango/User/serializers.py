from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from rest_framework import serializers

# from ScratchDjango.Profile.serializers import ProfileSerializer
from .constants import FRONTEND_URL, HOST
from .models import User
from .tasks import send_email
from .validators import check_email

# from .validators import check_email


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    email_plaintext_message = "Hi, You have initiated a password reset request. Click on the link below to reset your password. \n\n{}{}token={}".format(
        FRONTEND_URL, "reset/?confirm=true&", reset_password_token.key
    )

    send_email.delay(
        [reset_password_token.user.email],
        "Password Reset for {title}".format(title="Django Scratch"),
        email_plaintext_message,
    )


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[check_email])

    class Meta:
        model = User
        fields = ("id", "name", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
