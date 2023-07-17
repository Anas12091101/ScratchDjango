from django.contrib.auth.models import User
from django.db import models
from django.db.models import CharField
from django.db.models.signals import pre_save
from django.dispatch import receiver

# @receiver(pre_save, sender=User)
# def my_handler(sender, **kwargs):
#     print("here")
#     if sender.pk is None:  # create
#         print(sender)
#         otp = Otp.objects.create(user=sender)
        
# Create your models here.
class Otp(models.Model):
    otp_choices = [("GA", "Google Authenticator"), ("Email", "Email")]
    user = models.OneToOneField(to="User.User", on_delete=models.CASCADE)
    email_otp = CharField(max_length=6, null=True, blank=True)
    otp_enabled = CharField(choices=otp_choices, null=True, blank=True, max_length=255)
    otp_base32 = CharField(max_length=255, null=True, blank=True)
    otp_auth_url = CharField(max_length=255, null=True, blank=True)

    def __str__(self) -> str:
        return str(self.user.name) + " " +str(self.otp_enabled)