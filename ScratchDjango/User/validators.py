import re

from django.core.exceptions import ValidationError

from .models import User
from .regex import email_regex


def check_email(email):
    user = User.objects.filter(email=email)
    if user:
        raise ValidationError("Email already exists")
    if re.fullmatch(email_regex, email):
        return True
    raise ValidationError("Enter a valid Email")