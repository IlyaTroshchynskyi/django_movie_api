import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class MovieApiTestCase(APITestCase):

    def setUp(self) -> None:
        self.user_1 = User.objects.create_user('test', 'test@mail.ua', '12345')

    def test_api_jwt(self):

        url_obtain = reverse('token_obtain_pair')
        verification_url = reverse('token_verify')
        refresh_url = reverse('token_refresh')
        data = {
            "username": "test",
            "password": "12345"
        }
        json_data = json.dumps(data)
        resp = self.client.post(url_obtain, data=json_data,
                                content_type='application/json')

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue('refresh' in resp.data)
        self.assertTrue('access' in resp.data)
        access_token = resp.data['access']
        refresh_token = resp.data['refresh']
        resp = self.client.post(verification_url, {'token': access_token},
                                format='json')

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        resp = self.client.post(verification_url, {'token': 'test'},
                                format='json')

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

        resp = self.client.post(refresh_url, {'refresh': refresh_token},
                                format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
