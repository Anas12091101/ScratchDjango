from django.db import models

from ScratchDjango.Profile.models import Profile


# Create your models here.
class Message(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    message = models.TextField()
    room = models.CharField(max_length=30)

    def __str__(self) -> str:
        return str(self.id) + "_" + self.room
