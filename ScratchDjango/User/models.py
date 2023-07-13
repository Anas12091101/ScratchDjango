from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models import BooleanField, CharField, EmailField
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_rest_passwordreset.signals import reset_password_token_created

from .constants import HOST
from .managers import UserManager
from .utils import check_email, send_email


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    email_plaintext_message = "{}{}".format(
        HOST,
        reverse("confirm_reset_template", kwargs={"token": reset_password_token.key}),
        reset_password_token.key,
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
    otp_choices = [("GA", "Google Authenticator"), ("Email", "Email")]
    email_otp = CharField(max_length=6, null=True, blank=True)
    otp_enabled = CharField(choices=otp_choices, null=True, blank=True, max_length=255)
    otp_base32 = CharField(max_length=255, null=True, blank=True)
    otp_auth_url = CharField(max_length=255, null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_absolute_url(self) -> str:
        return reverse("users:detail", kwargs={"pk": self.id})

    def save(self, *args, **kwargs):
        try:
            # self.full_clean()
            super(User, self).save(*args, **kwargs)
        except IntegrityError as e:
            raise ValidationError(str(e))
