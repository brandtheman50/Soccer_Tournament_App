from rest_framework import serializers
from .models import *

from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import *

from users.serializers import UserSerializerModel

User = get_user_model()

class TeamSerializer(serializers.Serializer):
    name = serializers.CharField()

    def validate(self, data):
        if Team.objects.filter(name=data["name"]).exists():
            raise serializers.ValidationError("Team with provided name already exists.")
        return data  # ✅ this is required

    def create(self, validated_data):
        return Team.objects.create(**validated_data)

class TeamMembershipSerializer(serializers.ModelSerializer):
    user = UserSerializerModel()
    class Meta:
        model = TeamMembership
        fields = ('user', 'role')

class TeamSerializerModel(serializers.ModelSerializer):
    team_membership = TeamMembershipSerializer(many=True)

    class Meta:
        model = Team
        fields = ('name', 'team_membership')