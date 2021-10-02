from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from ..models import User


class UserTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username='testuser1', password='123',
            email='testuser1@yandex.ru'
        )

    def test_get_user_info_about_me(self):
        client = APIClient()
        client.force_authenticate(user=UserTest.user)
        response = client.get('/api/v1/users/me/')
        self.assertEqual(response.json()['email'], 'testuser1@yandex.ru')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_user_info_about_me(self):
        client = APIClient()
        client.force_authenticate(user=UserTest.user)
        response = client.patch(
            '/api/v1/users/me/',
            {'first_name': 'test',
             'last_name': 'user'}
        )
        self.assertEqual(response.json()['first_name'], 'test')
        self.assertEqual(response.json()['last_name'], 'user')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
