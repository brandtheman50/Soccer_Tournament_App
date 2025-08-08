from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import *
from .permissions import *

class RegisterTeam(APIView, BaseAuth):
    def post(self, request):
        serializer = TeamSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # DRF handles validation errors
        serializer.save()
        return Response({"message": "Team created successfully."}, status=201)
    
class TeamView(APIView, BaseAuth):
    def get(self, request):
        team_id = request.GET.get("team_id")

        # Fetch team with all users (players and admins)
        team = Team.objects.filter(id=team_id).prefetch_related("team_membership__user").first()

        if not team:
            return Response({"error": "Team not found"}, status=400)
        
        serializer = TeamSerializerModel(team, many=False)
        return Response(serializer.data)

class AssignUserToTeam(APIView):
    permission_classes = [IsTeamAdmin]

    def post(self, request):
        try:
            data = request.data
            user_id = data.get("user_id")
            team_id = data.get("team_id")
            role = data.get("role", "").lower()

            # Validate role
            if role not in dict(TeamMembership.ROLE_CHOICES):
                return Response({"error": "Invalid role."}, status=status.HTTP_400_BAD_REQUEST)

            # Fetch user and team instances
            user = User.objects.get(id=user_id)
            team = Team.objects.get(id=team_id)

            # Created will be false if user already assigned to team
            membership, created = TeamMembership.objects.get_or_create(
                user=user,
                team=team,
                defaults={"role": role}
            )

            if not created:
                return Response({"message": "User already in team."}, 200)

            return Response({"message": f"User added as {membership.role}."}, 201)

        except (User.DoesNotExist, Team.DoesNotExist):
            return Response({"error": "User or Team not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"error": "Something went wrong."}, status=status.HTTP_400_BAD_REQUEST)