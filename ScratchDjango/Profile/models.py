from django.db import models

from ScratchDjango.User.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default_avatar.png', upload_to='avatars')
    bio = models.TextField()

    def __str__(self):
        return self.user.name
