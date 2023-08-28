from django.contrib import admin

from .models import Membership, Subscription

# Register your models here.
admin.site.register(Subscription)
admin.site.register(Membership)
