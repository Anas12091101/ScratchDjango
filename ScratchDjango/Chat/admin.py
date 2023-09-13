from django.contrib import admin

from .models import FileMessage, Message

# Register your models here.
admin.site.register(Message)
admin.site.register(FileMessage)
