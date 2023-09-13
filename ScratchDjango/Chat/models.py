from django.db import models

from ScratchDjango.Profile.models import Profile
from ScratchDjango.User.models import User


# Create your models here.
class Message(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    message = models.TextField()
    type = models.CharField(max_length=100, default="text")
    room = models.CharField(max_length=30)

    def __str__(self) -> str:
        return str(self.id) + "_" + self.room


class FileMessage(models.Model):
    file_url = models.FileField(upload_to="message_files")
    file_type = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + "_" + self.user.name + "_" + self.file_type
