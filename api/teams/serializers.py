from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import *
from django.db.models import Exists, OuterRef

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
            "date_of_birth",
            "profile_photo",
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
    
    def validate(self, attrs):
        email = attrs.get("email", getattr(self.instance, "email", None))
        team  = attrs.get("team",  getattr(self.instance, "team",  None))

        team_standing = TeamStanding.objects.get(team=team, league__status=League.ACTIVE)
        league = team_standing.league

        qs = PlayerProfile.objects.filter(email=email)

        qs = qs.annotate(
            in_league=Exists(
                TeamStanding.objects.filter(
                    league=league,
                    team_id=OuterRef("team_id")
                )
            )
        ).filter(in_league=True)

        if qs.exists():
            raise ValueError("Email already in use.")
        return attrs

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