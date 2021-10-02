from rest_framework import status
from rest_framework.test import (APIClient, APIRequestFactory, APITestCase,
                                 force_authenticate)

from ..models import Account, User
from ..views import AccountViewSet


class AccountTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username='testuser', password='123'
        )

    def test_create_account(self):
        factory = APIRequestFactory()
        request = factory.post('/api/v1/accounts/')
        force_authenticate(request, user=AccountTests.user)
        view = AccountViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(str(Account.objects.first()), '1 - testuser - 0.00')
        self.assertEqual(Account.objects.count(), 1)

    def test_get_account(self):
        client = APIClient()
        client.force_authenticate(user=AccountTests.user)
        client.post('/api/v1/accounts/')
        response = client.get('/api/v1/accounts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['count'], 1)
