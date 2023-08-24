from django.http import JsonResponse
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken

from .exceptions import TokenExpiredException

# from django.core.exceptions import ValidationError

class JWTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # print(request)
        try:
            JWT_authenticator = JWTAuthentication()
            response = JWT_authenticator.authenticate(request)
            if response is not None:
                user , token = response
                print(user.last_token_iat, token.payload['iat'])
                if user.last_token_iat != token.payload['iat']:
                    raise TokenExpiredException("Token expired")
            response = self.get_response(request)
        except TokenExpiredException as e:
            print(e)
            response = JsonResponse({"message":str(e)}, status=status.HTTP_406_NOT_ACCEPTABLE)
        except InvalidToken as e:
            response = JsonResponse({"message":"token invalid"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            response = JsonResponse({"message":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return response
