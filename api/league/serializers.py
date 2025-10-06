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

class TeamStandingWriteSerializer(serializers.Serializer):
    # Write inputs
    league_id = serializers.PrimaryKeyRelatedField(
        source="league", queryset=League.objects.all(), write_only=True
    )

    team_id = serializers.PrimaryKeyRelatedField(
        source="team", 
        queryset=Team.objects.all(), 
        write_only=True, 
        allow_null=True
    )

    def create(self, validated_data):
        return TeamStanding.objects.create(**validated_data)