from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from ..models import Account, Service, Transaction, User


class TransactionTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username='testuser', password='123'
        )
        cls.account = Account.objects.create(
            user=cls.user,
            balance=100
        )
        cls.service = Service.objects.create(
            name='test123',
            description='test123',
            price=100,
            currency='RUB'
        )

    def test_create_transaction(self):
        client = APIClient()
        client.force_authenticate(user=TransactionTests.user)
        response = client.get('/api/v1/services/2/purchase/')
        self.assertEqual(Transaction.objects.count(), 1)
        self.assertEqual(
            str(Transaction.objects.first()),
            'Счет номер 4 приобрел услугу test123 за 100.00 RUB'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_transaction(self):
        client = APIClient()
        client.force_authenticate(user=TransactionTests.user)
        client.get('/api/v1/services/2/purchase/')
        response = client.get('/api/v1/transactions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['count'], 1)
