import os

from .base import *

DATABASES = {"default": env.db("DATABASE_URL", default="")}

SECRET_KEY = env("DJANGO_SECRET_KEY")

# Email Backend
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False


# Actual directory user files go to
MEDIA_ROOT = str(APPS_DIR / "media")

# URL used to access the media
MEDIA_URL = '/media/'