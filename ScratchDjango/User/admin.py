from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "is_active"]
    search_fields = ["name", "email"]
    list_filter = ["is_active"]


# Register your models here.
admin.site.register(User, UserAdmin)
