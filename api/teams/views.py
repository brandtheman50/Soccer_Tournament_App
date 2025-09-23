from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from django.template.loader import render_to_string


from .serializers import *
from .permissions import *

class RegisterPlayer(APIView):
    def post(self, request):
        data = request.data

        # Process file for photo and add path string to data

        serializer = PlayerProfileSerializer(data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(PlayerProfileSerializer(instance).data, status=status.HTTP_200_OK)