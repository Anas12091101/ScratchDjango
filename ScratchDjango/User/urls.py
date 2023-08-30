from django.urls import include, path

from .views import blacklist_token, login_user, register_user

urlpatterns = [
    path("register_user/", register_user, name="register_user"),
    path("login/", login_user, name="login"),
    path(
        "api/password_reset/",
        include("django_rest_passwordreset.urls", namespace="password_reset"),
    ),
    path("blacklist_token/", blacklist_token, name="blacklist_token"),
]
