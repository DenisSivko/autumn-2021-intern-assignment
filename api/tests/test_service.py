from rest_framework import status
from rest_framework.test import (APIRequestFactory, APITestCase,
                                 force_authenticate)

from ..models import Service, User
from ..views import ServiceViewSet


class ServiceTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username='testuser', password='123'
        )
        cls.service = Service.objects.create(
            name='test',
            description='test',
            price=100,
            currency='USD'
        )

    def test_create_service(self):
        factory = APIRequestFactory()
        request = factory.get('/api/v1/services/')
        force_authenticate(request, user=ServiceTests.user)
        view = ServiceViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(Service.objects.count(), 1)
        self.assertEqual(str(Service.objects.first()), 'test')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
