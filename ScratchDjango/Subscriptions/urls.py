from django.urls import path

from .views import get_membership_details, subscribe

urlpatterns = [
    path("get_memberships/",get_membership_details,name="get_memberships"),
    path("subscribe/",subscribe, name="subscribe")
]