import magic
from django.conf import settings
from rest_framework import serializers


def validate_image(image):
    extension = image.name.split('.')[-1]
    content_type = image.content_type
    if not extension or extension.lower() not in settings.WHITELISTED_IMAGE_TYPES.keys():
        raise serializers.ValidationError("invalid image extension")
    if image.size > settings.UPLOAD_FILE_MAX_SIZE:
        raise serializers.ValidationError("size {} larger than 1 MB".format(image.size))
    if content_type not in settings.WHITELISTED_IMAGE_TYPES.values():
        raise serializers.ValidationError("invalid image content-type")
    mime_type = magic.from_buffer(image.read(1024), mime=True)
    if mime_type not in settings.WHITELISTED_IMAGE_TYPES.values() and mime_type != content_type:
        raise serializers.ValidationError("invalid image mime-type")
