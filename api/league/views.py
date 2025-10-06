from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
from .models import Match

from .services.match_services import *
from datetime import datetime
from .serializers import *
from .permissions import IsLeagueAdmin

# Create your views here.

class CreateMatch(APIView, IsLeagueAdmin):
    def post(self, request):
        try:
            data = request.data
            serializer = MatchSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(status=200)
        except Exception as e:
            return Response({"error": "Something went wrong"}, status=400)
        
class UpdateMatch(APIView, IsLeagueAdmin):
    @transaction.atomic
    def patch(self, request):
        try:
            data = request.data
            match_id = data.get("match_id")
            match = Match.objects.get(id=match_id)
            
            # Rollback previous results
            rollback_standings(match)

            # Update new results
            home_score = data.get("home_score")
            away_score = data.get("away_score")
            field_name = data.get("field_name")
            address = data.get("address")
            scheduled_date = data.get("scheduled_date")

            match.home_score = home_score
            match.away_score = away_score
            match.field_name = field_name
            match.address = address

            # Store naive scheduled_date
            # DO NOT CONVERT TO ANOTHER TIMEZONE
            # Timezone will be determined based on the city stored in address
            match.scheduled_date = datetime.strptime(scheduled_date, "%Y-%m-%dT%H:%M")

            match.save()
            update_standings_for_match(match)

        except Match.DoesNotExist:
            return Response({"error": "Match not found"}, status=404)
        except Exception as e:
            return Response({"error": "Something went wrong"})

class CreateLeague(APIView, IsLeagueAdmin):
    def post(self, request):
        data = request.data
        serializer = LeagueSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "League created successfully."})

class AddTeamToLeague(APIView, IsLeagueAdmin):
    def post(self, request):
        """
        # Create a standing with an existing team:       
        {
            "league_id": 3,
            "team_id": 42
        }

        # Create a new team + standing
        {
            "league_id": 3,
            "team_payload": {
                "name": "Blue Tigers",
                "logo_file_path": "/logos/blue_tigers.png",
                "is_paid": true
            }
        }
        """

        data = request.data
        serializer = TeamStandingCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=200)