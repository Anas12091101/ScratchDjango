from django.urls import path

from .views import get_membership_details

urlpatterns = [
    path("get_memberships/",get_membership_details,name="get_memberships")
]