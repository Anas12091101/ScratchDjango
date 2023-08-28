import re

from django.core.exceptions import ValidationError

from .regex import email_regex


def check_email(email):
    if re.fullmatch(email_regex, email):
        return True
    raise ValidationError("Enter a valid Email")