from rest_framework import serializers
from .models import *

class LeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = League
        fields = [
            "id",
            "name",
            "created_at",
            "updated_at",
            "status"
        ]
        read_only_fields = ["id", "created_at", "updated_at", "status"]
    def create(self, validated_data):
        return League.objects.create(**validated_data)

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

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'

class TeamWriteSerializer(serializers.Serializer):
    name = serializers.CharField()
    logo_file_path = serializers.CharField(max_length=50)
    is_paid = serializers.BooleanField(default=False)

class TeamStandingCreateSerializer(serializers.ModelSerializer):
    # Write inputs
    league_id = serializers.PrimaryKeyRelatedField(
        source="league", queryset=League.objects.all(), write_only=True
    )
    team_payload = TeamWriteSerializer(write_only=True, required=False)

    team_id = serializers.PrimaryKeyRelatedField(
        source="team", 
        queryset=Team.objects.all(), 
        write_only=True, 
        required=False, 
        allow_null=True
    )
    # READ output
    team = TeamSerializer(read_only=True)

    class Meta:
        model = TeamStanding
        fields = [
            "id",
            "team",
            "league",
            "league_id",
            "team_id",
            "team_payload",
            "matches_played", "wins", "losses", "draws",
            "goals_for", "goals_against"
        ]
        read_only_fields = ["league", "matches_played", "wins", "losses", "draws", "goals_for", "goals_against"]

    def validate(self, attrs):
        # Ensure exactly one of team_id or team_payload is provided
        has_team_id = "team" in attrs
        has_team_payload = "team_payload" in attrs
        if has_team_id == has_team_payload:
            raise serializers.ValidationError(
                {"team": "Provide exactly one of 'team_id' or 'team_payload'."}
            )
        return attrs
    
    # @transaction.atomic
    def create(self, validated_data):
        league = validated_data.pop("league")
        team = validated_data.pop("team", None)
        team_payload = validated_data.pop("team_payload", None)

        # If a new team is being created
        if team is None:
            team = Team.objects.create(**team_payload)
        
        # Enforce unique (team, league) - your DB constraint will guard this too
        if TeamStanding.objects.filter(team=team, league=league).exists():
            raise serializers.ValidationError(
                {"non_field_errors": ["This team already has a standing in this league."]}
            )
        return TeamStanding.objects.create(team=team, league=league, **validated_data)