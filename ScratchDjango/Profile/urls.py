from django.urls import path

from .views import get_user_profile, update_profile

urlpatterns = [
    path("update_profile", update_profile, name="create_profile"),
    path("get_profile", get_user_profile, name="get_profile"),
]
