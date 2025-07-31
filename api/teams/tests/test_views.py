from rest_framework.test import APIRequestFactory
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase
from teams.views import RegisterTeam

class RegisterTeamTest(TestCase):
    def setup(self):
        self.factory = APIRequestFactory()
    
    def test_details(self):
        data = {
            "name": "ATI FC",
            "coach_first_name": "Brandon",
            "coach_last_name": "Altamirano",
            "contact_phone": "6195558888",
            "contact_email": "manabran501@hotmail.com"
        }

        # Create an instance of a POST request
        request = self.factory.post('/register', data, content_type='application/json')
        request.user = AnonymousUser()

        response = RegisterTeam.as_view()(request)
        self.assertEqual(response.status_code, 200)