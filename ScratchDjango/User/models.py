from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models import BooleanField, CharField, EmailField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .managers import UserManager
from .utils import check_email


class User(AbstractUser):
    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    email = EmailField(_("email address"), unique=True, validators=[check_email])
    username = None  # type: ignore
    otp_enabled = BooleanField(default=False)
    otp_base32 = CharField(max_length=255, null=True, blank=True)
    otp_auth_url = CharField(max_length=255, null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_absolute_url(self) -> str:
        return reverse("users:detail", kwargs={"pk": self.id})

    def save(self, *args, **kwargs):
        try:
            self.full_clean()
            super(User, self).save(*args, **kwargs)
        except IntegrityError as e:
            raise ValidationError(str(e))
