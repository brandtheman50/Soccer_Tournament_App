from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from django.core.mail import send_mail

from .serializers import *

class RegisterTeam(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = TeamSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
class RegisterPlayer(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = PlayerSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

class GetTeam(APIView):
    def get(self, request, team_id):
        try:
            team = Team.objects.filter(id=team_id).prefetch_related("team_players").first()
            serializer = OutputTeamSerializer(team)
            return Response(serializer.data)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

class GetPlayer(APIView):
    def get(self, request, player_id):
        try:
            player = Player.objects.filter(id=player_id).select_related("team").first()
            serializer = PlayerSerializer(player)
            return Response(serializer.data)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

class GenerateQRCode(APIView):
    def get(self, request, team_id, player_id):
        try:
            team = Team.objects.get(id=team_id)
            player = Player.objects.get(id=player_id)
            
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)