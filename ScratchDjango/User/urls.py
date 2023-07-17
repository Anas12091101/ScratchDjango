from django.urls import include, path

from .views import check_login, check_otp, login_user, register_user

urlpatterns = [
    path("register_user/", register_user, name="register_user"),
    path("login/", login_user, name="login"),
    path("check_login/", check_login, name="check_login"),
    path("check_otp/", check_otp, name="check_otp"),
    path(
        "api/password_reset/",
        include("django_rest_passwordreset.urls", namespace="password_reset"),
    ),
]