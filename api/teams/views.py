from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from email.mime.image import MIMEImage

from .serializers import *
from .permissions import *

import qrcode

from io import BytesIO

from core.env import API_HOSTNAME

from users.models import User

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
        
class GenerateQRCode(APIView):
    def get(self, request, team_id, player_id):
        try:
            team = Team.objects.get(id=team_id)
            user = User.objects.get(id=player_id)
            
            # Verify user is assigned to team
            TeamMembership.objects.get(team=team, user=user)
            
            # Data to encode in the QR code
            url = f"{API_HOSTNAME}/users/get-user/{user.id}"

            # Generate the QR code
            img = qrcode.make(url)
            buf = BytesIO()
            img.save(buf, format="PNG")
            png_bytes = buf.getvalue()

            # Render HTML template; reference the image by a CID
            html = render_to_string("emails/qr_code_email.html", context={"qr_cid": "qr1"})

            # Build email
            subject = "Your QR Code"
            text_fallback = "Your email client doesn't support HTML. The QR code is attached."
            email = EmailMultiAlternatives(subject, text_fallback, to=[user.email])
            email.attach_alternative(html, "text/html")

            # Attach PNG inline with a matching CID
            img_part = MIMEImage(png_bytes, _subtype="png")
            img_part.add_header("Content-ID", "<qr1>")
            img_part.add_header("Content-Disposition", "inline", filename="qr.png")
            email.attach(img_part)

            # 5) Send
            email.send()

            return Response(status=status.HTTP_200_OK)

        except TeamMembership.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)