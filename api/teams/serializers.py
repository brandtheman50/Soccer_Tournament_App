from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import *

from league.models import League, TeamStanding

from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import *

from users.serializers import UserSerializerModel

User = get_user_model()

class TeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Team
        fields = ["id", "name"]

class PlayerProfileSerializer(serializers.ModelSerializer):
    # Accept a team id on write, expose a nested or pk on read
    team_id = serializers.PrimaryKeyRelatedField(
        source="team", queryset=Team.objects.all(), write_only=True
    )

    # If you want to display the team pk back:
    team = TeamSerializer(read_only=True)
    
    class Meta:
        model = PlayerProfile
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "team", # read-only view of the relation
            "team_id", # write-only input
        ]
        validators = [
            UniqueTogetherValidator(
                queryset=PlayerProfile.objects.all(),
                fields=["team", "email"],
                message="This email is already registered in this team."
            )
        ]

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