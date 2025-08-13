from django.urls import path
from .views import *

urlpatterns = [
    path('create-match', CreateMatch.as_view(), name="create_match"),
    path('update-match', UpdateMatch.as_view(), name="update_match"),
    path('create-league', CreateLeague.as_view(), name="create_league"),
    path('add-team-league', AddTeamToLeague.as_view(), name="add_team_league")
]