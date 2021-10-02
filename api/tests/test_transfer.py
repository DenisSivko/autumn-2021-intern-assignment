from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from ..models import Account, Transfer, User


class TransferTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user1 = User.objects.create_user(
            username='testuser1', password='123',
            email='testuser1@yandex.ru'
        )
        cls.user2 = User.objects.create_user(
            username='testuser2', password='123',
            email='testuser2@yandex.ru'
        )
        cls.account1 = Account.objects.create(
            user=cls.user1,
            balance=100
        )
        cls.account2 = Account.objects.create(
            user=cls.user2,
            balance=100
        )

    def test_create_transfer(self):
        client = APIClient()
        client.force_authenticate(user=TransferTests.user1)
        response = client.post(
            '/api/v1/transfers/',
            {'from_account': '5',
             'to_account': '6',
             'amount': '100'}
        )
        self.assertEqual(Transfer.objects.count(), 1)
        self.assertEqual(
            str(Transfer.objects.first()),
            ('Перевод с 5 - testuser1 - 0.00 на 6 - testuser2 - 200.00, '
             'сумма перевода 100.00')
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_transfer(self):
        client = APIClient()
        client.force_authenticate(user=TransferTests.user1)
        client.post(
            '/api/v1/transfers/',
            {'from_account': '5',
             'to_account': '6',
             'amount': '100'}
        )
        response = client.get('/api/v1/transfers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['count'], 1)

    def test_get_transfer_to_my_account(self):
        client1 = APIClient()
        client2 = APIClient()
        client1.force_authenticate(user=TransferTests.user1)
        client2.force_authenticate(user=TransferTests.user2)
        client1.post(
            '/api/v1/transfers/',
            {'from_account': '5',
             'to_account': '6',
             'amount': '100'}
        )
        response = client2.get('/api/v1/transfers/to_my_account/')
        self.assertEqual(Transfer.objects.count(), 1)
        self.assertEqual(response.json()['count'], 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
