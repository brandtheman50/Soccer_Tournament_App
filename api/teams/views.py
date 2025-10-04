from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .helpers import send_qr_email


from .serializers import *
from .permissions import *

class RegisterPlayer(APIView):
    def post(self, request):
        data = request.data

        # Process file for photo and add path string to data

        serializer = PlayerProfileSerializer(data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        player_data = serializer.data
        send_qr_email(player_data.email, str(player_data.id))

        return Response(status=status.HTTP_200_OK)