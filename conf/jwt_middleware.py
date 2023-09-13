from django.core.cache import cache
from django.http import JsonResponse
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken

from .exceptions import TokenExpiredException


class JWTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            JWT_authenticator = JWTAuthentication()
            response = JWT_authenticator.authenticate(request)
            if response is not None:
                user, token = response
                last_token = cache.get(token)
                if last_token:
                    raise TokenExpiredException("Token expired")
            response = self.get_response(request)
        except TokenExpiredException as e:
            response = JsonResponse({"message": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except InvalidToken as e:
            response = JsonResponse(
                {"message": "token invalid"}, status=status.HTTP_401_UNAUTHORIZED
            )
        except Exception as e:
            response = JsonResponse(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return response
