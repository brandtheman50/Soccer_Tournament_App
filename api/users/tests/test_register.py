# tests/test_register.py
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory
from users.views import RegisterUser  # your APIView

@pytest.mark.django_db
def test_register_user_with_factory():
    factory = APIRequestFactory()
    url = reverse("register-user")
    request = factory.post(url, {
        "first_name": "Test",
        "last_name": "User",
        "email": "test@gmail.com",
        "username": "testuser",
        "phone": "6195558888",
        "password": "Rocko2012$",
    }, format="json")  # use format instead of content_type

    response = RegisterUser.as_view()(request)
    assert response.status_code == status.HTTP_200_OK
