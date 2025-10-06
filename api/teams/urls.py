from django.urls import path
from .views import *

urlpatterns = [
    path('register-player', RegisterPlayer.as_view(), name="register-player")
]