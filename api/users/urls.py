from django.urls import path
from .views import *
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('register', RegisterUser.as_view(), name="register"),
    path('token/', obtain_auth_token),
]