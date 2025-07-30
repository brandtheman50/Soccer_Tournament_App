from rest_framework import serializers
from .models import *

class TeamSerializer(serializers.Serializer):
    name = serializers.CharField()
    coach_name = serializers.CharField()
    contact_phone = serializers.CharField()
    contact_email = serializers.CharField()

class PlayerSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    contact_phone = serializers.CharField()
    contact_email = serializers.CharField()
    team = serializers.IntegerField()
    date_of_birth = serializers.DateField()

class OutputPlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'

class OutputTeamSerializer(serializers.ModelSerializer):
    team_players = OutputPlayerSerializer(many=True)
    class Meta:
        model = Team
        fields = '__all__'