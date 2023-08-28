import random
from datetime import datetime, timedelta

import jwt
from celery import current_app
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken

from .tasks import perform_logout, send_email


def get_refresh_token(user):
    refresh = RefreshToken.for_user(user)
    payload = jwt.decode(str(refresh.access_token), settings.SECRET_KEY, algorithms=["HS256"])
    user.last_token_iat = payload["iat"]
    user.save()
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


def calculate_logout_time(duration):
    return datetime.now() + timedelta(seconds=duration * 30)


def start_logout_timer(user):
    if (
        user.logout_task_id != "NA"
    ):  # If a logout task is already scheduled, we need to revoke it, because we have a new signin
        current_app.control.revoke(user.logout_task_id)

    logout_time = calculate_logout_time(user.subscription.membership.login_hours)
    task = perform_logout.apply_async(args=[user.id], eta=logout_time)
    user.logout_task_id = task.id
    user.save()
