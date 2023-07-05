from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Membership, Subscription
from .serializers import MembershipSerializer


@api_view(["GET"])
def get_membership_details(request):
    memberships = Membership.objects.all()
    serializer = MembershipSerializer(memberships, many=True)
    return Response(serializer.data)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def subscribe(request):
    data = request.data
    id = data["id"]
    membership = Membership.objects.get(id=id)
    subscription = Subscription.objects.create(user=request.user,membership=membership,expire_date=None)
    subscription.save()
    return Response({"status":"subscription activated"})