from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "is_active"]
    search_fields = ["name", "email", "is_active"]


# Register your models here.
admin.site.register(User, UserAdmin)
