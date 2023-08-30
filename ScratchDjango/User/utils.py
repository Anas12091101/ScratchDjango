from datetime import datetime, timedelta

from celery import current_app
from rest_framework_simplejwt.tokens import RefreshToken

from .tasks import perform_logout


def get_refresh_token(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


def calculate_logout_time(duration):
    return datetime.now() + timedelta(seconds=duration * 15)


# Starts logout timer based on user's subscription
def start_logout_timer(user, token):
    if (
        user.logout_task_id != "NA"
    ):  # If a logout task is already scheduled, we need to revoke it, because we have a new signin
        current_app.control.revoke(user.logout_task_id)

    logout_time = calculate_logout_time(user.subscription.membership.login_hours)
    task = perform_logout.apply_async(args=[user.id, token], eta=logout_time)
    user.logout_task_id = task.id
    user.save()
