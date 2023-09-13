from django.urls import path

from .views import upload_file, validate_room

urlpatterns = [
    path("validate_room", validate_room, name="validate_room"),
    path("upload_file", upload_file, name="upload_file"),
]
