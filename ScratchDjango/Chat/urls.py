from django.urls import path

from .views import validate_room

urlpatterns = [path("validate_room", validate_room, name="validate_room")]
