from django.urls import path

from .views import (
    check_login,
    check_login_template,
    login_template,
    login_user,
    register_user,
    register_user_template,
)

urlpatterns = [
    path("register_user/", register_user, name="register_user"),
    path("login/", login_user, name="login"),
    path("check_login/", check_login, name="check_login"),
]
template_url_patterns = [
    path("register_user_template/", register_user_template, name="register_user_template"),
    path("login_template/", login_template, name="login_template"),
    path("check_login_template/<str:token>", check_login_template, name="check_login_template"),
]
urlpatterns += template_url_patterns
