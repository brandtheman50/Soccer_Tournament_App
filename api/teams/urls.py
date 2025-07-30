from django.urls import path
from .views import *

urlpatterns = [
    path('register_team', RegisterTeam.as_view(), name="register_team"),
    path('register_player', RegisterPlayer.as_view(), name="register_player"),
    path('get_team', GetTeam.as_view(), name="get_team"),
    path('get_player', GetPlayer.as_view(), name="get_player")
]