from django.urls import path

from .views import register_user, register_user_template

urlpatterns = [
    path("register_user/", register_user, name="register_user"),
]
template_url_patterns = [
    path("register_user_template/", register_user_template, name="register_user_template"),
]
urlpatterns += template_url_patterns
