from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Membership, Subscription
from .serializers import MembershipSerializer
from .utils import capture_order, create_order


@api_view(["GET"])
def get_membership_details(request):
    memberships = Membership.objects.all()
    serializer = MembershipSerializer(memberships, many=True)
    return Response(serializer.data)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_membership(request):
    user = request.user
    # subscription = Subscription.objects.get(user=user)
    membership = user.subscription.membership
    serializer = MembershipSerializer(membership, many=False)
    return Response(serializer.data)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_paypal_order(request):
    data = request.data
    response = create_order(price=data["price"])
    return Response(response)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def capture_paypal_order(request):
    data = request.data
    response = capture_order(data["orderId"])
    transaction = response["purchase_units"][0]["payments"]["captures"][0]
    if transaction["status"] == "COMPLETED":
        user = request.user
        subscription = Subscription.objects.get(user=user)
        membership = Membership.objects.get(id=data["memberId"])
        if subscription:
            subscription.membership = membership
        else:    
            subscription = Subscription.objects.create(user=request.user,membership=membership,expire_date=None)
        subscription.save()

    return Response(response)