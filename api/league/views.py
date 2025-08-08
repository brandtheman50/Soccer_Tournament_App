from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
from .models import Match

from services.match_services import *
from datetime import datetime
# Create your views here.

class UpdateMatch(APIView):
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