from rest_framework import serializers
from .models import *

class LeagueSerializer(serializers.Serializer):
    name = serializers.CharField()

class MatchSerializer(serializers.Serializer):
    league = serializers.IntegerField()
    home_team = serializers.IntegerField()
    away_team = serializers.IntegerField()
    field_name = serializers.CharField()
    address = serializers.CharField()
    scheduled_date = serializers.DateTimeField()
    home_score = serializers.IntegerField(required=False)
    away_score = serializers.IntegerField(required=False)

    def validate(self, data):
        if data["home_team"] == data["away_team"]:
            raise serializers.ValidationError(
                {"away_team": "Home and away teams must be different"}
            )
    def create(self, validated_data):
        return Match.objects.create(**validated_data)
    
class TeamStandingSerializer(serializers.Serializer):
    team = serializers.IntegerField()
    league = serializers.IntegerField()

    def validate(self, data):
        if Team.objects.filter(team=data["team"], league=data["leage"]).exists():
            raise serializers.ValidationError(
                {"error": "This team has already been added to league."}
            )
    def create(self, validated_data):
        return TeamStanding.objects.create(**validated_data)