from datetime import datetime

from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.authtoken.models import Token


User = get_user_model()


def test_create(api_client, fixt_user):
    data = {
        'start_date': datetime(2017, 2, 12, 17, 00),
        'end_date': datetime(2017, 2, 12, 17, 20),
        'theme': 'THEME',
        'description': 'desc',
    }
    response = api_client.post('/reservation/', data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    credentials = {
        'username': fixt_user.username,
        'password': 'secret',
    }
    response = api_client.post('/api-auth/', credentials)
    print(credentials, response.data)
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + response.data['token'])

    response = api_client.post('/reservation/', data)
    assert response.status_code == status.HTTP_201_CREATED
