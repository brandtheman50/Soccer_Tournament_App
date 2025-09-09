from rest_framework.test import APIRequestFactory

# Create your tests here.

def test_register_user():

    factory = APIRequestFactory()
    request = factory.post('/register', {
        'first_name': 'Test',
        'last_name': 'User',
        'email': 'test@gmail.com',
        'username': 'testuser',
        'phone': '6195558888',
        'password': 'Rocko2012$'
    }, content_type='application/json')