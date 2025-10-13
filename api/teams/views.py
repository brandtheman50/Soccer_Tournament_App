from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.db import transaction

from .helpers import send_qr_email


from .serializers import *
from .permissions import *

class PlayerMethods(APIView):
    @transaction.atomic
    def post(self, request):
        data = request.data

        # Process file for photo and add path string to data

        serializer = PlayerProfileSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        player_data = serializer.data
        send_qr_email(player_data.get("email"), str(player_data.get("id")))

        return Response(status=status.HTTP_200_OK)
    
    def get(self, request):
        player_uuid = request.GET.get("player")

        # Handle image url generation
        player = PlayerProfile.objects.get(public_id=player_uuid)
        serializer = PlayerProfileSerializer(player)
        return Response(serializer.data)

