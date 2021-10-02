from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (AccountViewSet, ActionViewSet, ServiceViewSet,
                    TransactionViewSet, TransferViewSet, UserViewSet,
                    send_confirmation_code, send_jwt_token)

router_v1 = DefaultRouter()
router_v1.register(
    'users',
    UserViewSet, basename='users'
)
router_v1.register(
    'accounts',
    AccountViewSet, basename='accounts'
)
router_v1.register(
    'actions',
    ActionViewSet, basename='actions'
)
router_v1.register(
    'services',
    ServiceViewSet, basename='services'
)
router_v1.register(
    'transactions',
    TransactionViewSet, basename='transactions'
)
router_v1.register(
    'transfers',
    TransferViewSet, basename='transfers'
)

auth_patterns = [
    path('email/', send_confirmation_code),
    path('token/', send_jwt_token),
]

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/', include(auth_patterns)),
]
