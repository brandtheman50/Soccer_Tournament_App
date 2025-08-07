from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import *

class RegisterTeam(APIView):
    def post(self, request):
        serializer = TeamSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # DRF handles validation errors
        serializer.save()
        return Response({"message": "Team created successfully."}, status=201)

class AssignUserToTeam(APIView):
    def post(self, request):
        try:
            user_id = request.GET.get("user_id")
            team_id = request.GET.get("team_id")
            role = request.GET.get("role", "").lower()

            # Validate role
            if role not in dict(TeamMembership.ROLE_CHOICES):
                return Response({"error": "Invalid role."}, status=status.HTTP_400_BAD_REQUEST)

            # Fetch user and team instances
            user = User.objects.get(id=user_id)
            team = Team.objects.get(id=team_id)

            # Create membership
            TeamMembership.objects.create(
                user=user,
                team=team,
                role=role
            )
            return Response(status=status.HTTP_201_CREATED)

        except (User.DoesNotExist, Team.DoesNotExist):
            return Response({"error": "User or Team not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"error": "Something went wrong."}, status=status.HTTP_400_BAD_REQUEST)
