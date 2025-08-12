from rest_framework.permissions import BasePermission
from rest_framework.permissions import IsAuthenticated

class IsLeagueAdmin(BasePermission):
    permission_classes = [IsAuthenticated]
    
    def has_permission(self, request, view):
        if not request.user.groups.filter(name__in=["LeagueAdmin"]):
            return False