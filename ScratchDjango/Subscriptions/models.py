import datetime

from dateutil.relativedelta import relativedelta
from django.db import models
from django.db.models import JSONField
from django.db.models.signals import post_save
from django.dispatch import receiver

from ScratchDjango.User.models import User

# Create your models here.

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        membership = Membership.objects.get(membership_type="free")
        Subscription.objects.create(user=instance, membership=membership)
        


class Membership(models.Model):
    membership_choices = (
        ("free", "Free"),
        ("standard","Standard"),
        ("pre","Premium"),
    )
    period_choices = (
        ("m","month"),
        ("y","year")
    )
    membership_type = models.CharField(
    choices=membership_choices, default="free",
    max_length=30
      )
    price = models.DecimalField(default=0.0, max_digits=10, decimal_places=3)
    period = models.CharField(choices=period_choices, max_length=20)
    features = JSONField()
    login_hours = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ("id",)
    def __str__(self):
       return str(self.membership_type)+"_"+self.period
    

class Subscription(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    membership = models.ForeignKey(Membership,on_delete=models.SET_NULL,null=True)
    expire_date = models.DateField(null=True)

    def save(self, *args, **kwargs):
        period = self.membership.period
        if period == "m":
            self.expire_date = datetime.date.today() + relativedelta(months=1)
        else:
            self.expire_date = datetime.date.today() + relativedelta(years=1)
        return super(Subscription,self).save(*args,**kwargs)
