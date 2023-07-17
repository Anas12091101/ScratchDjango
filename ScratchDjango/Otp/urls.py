from django.urls import path

from .views import check_otp, create_otp

urlpatterns = [path("check/",check_otp, name="check_otp"),
               path("create/",create_otp,name="create_otp")]