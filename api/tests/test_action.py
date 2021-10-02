from rest_framework import status
from rest_framework.test import (APIClient, APIRequestFactory, APITestCase,
                                 force_authenticate)

from ..models import Account, Action, User
from ..views import ActionViewSet


class ActionTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username='testuser', password='123'
        )
        cls.account = Account.objects.create(
            user=cls.user
        )

    def test_create_action(self):
        factory = APIRequestFactory()
        request = factory.post(
            '/api/v1/actions/',
            {'amount': '1000',
             'account': '3'}
        )
        force_authenticate(request, user=ActionTests.user)
        view = ActionViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            str(Action.objects.first()),
            'Счет номер 3 был пополнен на 1000.00 руб.'
        )
        self.assertEqual(Action.objects.count(), 1)
        self.assertEqual(
            Account.objects.get(user=ActionTests.user).balance, 1000
        )

    def test_get_account(self):
        client = APIClient()
        client.force_authenticate(user=ActionTests.user)
        client.post(
            '/api/v1/actions/',
            {'amount': '1000',
             'account': '3'}
        )
        response = client.get('/api/v1/actions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['count'], 1)
