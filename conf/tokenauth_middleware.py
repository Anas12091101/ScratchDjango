from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken

from ScratchDjango.User.models import User


@database_sync_to_async
def get_user(token_key):
    token = AccessToken(token_key)
    user_id = token["user_id"]
    user = User.objects.get(id=user_id)
    return user


class TokenAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        try:
            token_key = (
                dict((x.split("=") for x in scope["query_string"].decode().split("&")))
            ).get("token", None)
        except ValueError:
            token_key = None
        scope["user"] = AnonymousUser() if token_key is None else await get_user(token_key)
        return await self.app(scope, receive, send)
