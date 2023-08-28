from django.urls import path

from .views import create_or_update

urlpatterns = [
    path("create_profile",create_or_update,name="create_profile")
]