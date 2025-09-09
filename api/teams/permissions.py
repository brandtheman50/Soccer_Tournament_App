from rest_framework.permissions import BasePermission
from .models import TeamMembership
from rest_framework.permissions import IsAuthenticated

# Inherit in each view
class BaseAuth:
    permission_classes = [IsAuthenticated]

class IsTeamAdmin(BasePermission):
    """
    Custom permission to check if the requesting user is an admin for the given team.
    """

    def has_permission(self, request, view):
        team_id = request.data.get("team_id") or request.GET.get("team_id")

        if not team_id or not request.user.is_authenticated:
            return False

        return TeamMembership.objects.filter(
            team_id=team_id,
            user=request.user,
            role="admin"
        ).exists()