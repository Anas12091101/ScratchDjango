from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models import BooleanField, CharField, EmailField, IntegerField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_rest_passwordreset.signals import reset_password_token_created

from ScratchDjango.Otp.models import Otp

from .constants import FRONTEND_URL, HOST
from .managers import UserManager
from .utils import send_email
from .validators import check_email


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    email_plaintext_message = "Hi, You have initiated a password reset request. Click on the link below to reset your password. \n\n{}{}token={}".format(
        FRONTEND_URL,
        "reset/?confirm=true&",
        reset_password_token.key
    )

    send_email(
        [reset_password_token.user.email],
        "Password Reset for {title}".format(title="Django Scratch"),
        email_plaintext_message,
    )


class User(AbstractUser):
    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    email = EmailField(_("email address"), unique=True, validators=[check_email])
    username = None  # type: ignore
    last_token_iat = IntegerField(null=True) # field for storing token generate time at auth
   
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_absolute_url(self) -> str:
        return reverse("users:detail", kwargs={"pk": self.id})

    def save(self, *args, **kwargs):
        try:
            super(User, self).save(*args, **kwargs)
        except IntegrityError as e:
            raise ValidationError(str(e))
