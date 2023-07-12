from django.urls import path

from .views import (
    capture_paypal_order,
    create_paypal_order,
    get_membership_details,
    get_user_membership,
)

urlpatterns = [
    path("get_memberships/",get_membership_details,name="get_memberships"),
    path("user_membership/",get_user_membership, name="user_membership"),
    path("create_paypal_order/",create_paypal_order, name="create_paypal_order"),
    path("capture_paypal_order/",capture_paypal_order, name="capture_paypal_order")

]