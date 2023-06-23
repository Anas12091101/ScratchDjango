from django.urls import include, path

from .views import (
    check_login,
    check_login_template,
    check_otp,
    confirm_reset_template,
    login_template,
    login_user,
    otp_template,
    register_user,
    register_user_template,
    reset_template,
)

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
template_url_patterns = [
    path("register_user_template/", register_user_template, name="register_user_template"),
    path("login_template/", login_template, name="login_template"),
    path("check_login_template/<str:token>", check_login_template, name="check_login_template"),
    path("otp_template/<str:email>", otp_template, name="otp_template"),
    path(
        "confirm_reset_template/<str:token>", confirm_reset_template, name="confirm_reset_template"
    ),
    path("reset_template/", reset_template, name="reset_template"),
]
urlpatterns += template_url_patterns
