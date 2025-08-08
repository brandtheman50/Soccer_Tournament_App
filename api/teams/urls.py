from django.urls import path
from .views import *

urlpatterns = [
    path('register', RegisterTeam.as_view(), name="register_team"),
    path('get-team', TeamView.as_view(), name="get_team"),
    path('assign-user', AssignUserToTeam.as_view(), name="assign_user_team")
]