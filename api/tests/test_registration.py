from django.contrib.auth.tokens import default_token_generator
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import User


class RegistrationTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username='testuser1', password='123',
            email='testuser1@yandex.ru'
        )

    def test_auth_email(self):
        response = self.client.post(
            '/api/v1/auth/email/',
            {'email': 'testuser@yandex.ru'}
        )
        self.assertEqual(
            response.json()['result'], 'Код подтверждения успешно отправлен!'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_auth_token(self):
        user = User.objects.filter(email='testuser1@yandex.ru').first()
        confirmation_code = default_token_generator.make_token(user)
        response = self.client.post(
            '/api/v1/auth/token/',
            {'email': 'testuser1@yandex.ru',
             'confirmation_code': str(confirmation_code)}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
