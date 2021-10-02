import decimal

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .models import Account, Service, Transaction, Transfer, User
from .permissions import IsAdmin, IsAdminOrReadOnly
from .serializers import (AccountEURSerializer, AccountSerializer,
                          AccountUSDSerializer, ActionSerializer,
                          EmailSerializer, ServiceSerializer, TokenSerializer,
                          TransactionSerializer, TransferSerializer,
                          UserSerializer)

USD_RATE = 72.56
EURO_RATE = 85.46
RUB_RATE = 1
CURRENCY_INFO = {
    'RUB': ('руб', RUB_RATE),
    'USD': ('USD', USD_RATE),
    'EUR': ('Euro', EURO_RATE),
}


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def send_confirmation_code(request):
    serializer = EmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data.get('email')
    if not User.objects.filter(email=email).exists():
        User.objects.create(
            username=email, email=email
        )
    user = User.objects.filter(email=email).first()
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        'Код подтверждения API',
        f'Ваш код подтверждения: {confirmation_code}',
        settings.DEFAULT_FROM_EMAIL,
        [email]
    )
    return Response(
        {'result': 'Код подтверждения успешно отправлен!'},
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def send_jwt_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data.get('email')
    confirmation_code = serializer.validated_data.get(
        'confirmation_code'
    )
    user = get_object_or_404(User, email=email)
    if default_token_generator.check_token(user, confirmation_code):
        token = AccessToken.for_user(user)
        return Response(
            {'token': str(token)}, status=status.HTTP_200_OK
        )
    return Response(
        {'confirmation_code': 'Неверный код подтверждения!'},
        status=status.HTTP_400_BAD_REQUEST
    )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [IsAdmin]
    filter_backends = [filters.SearchFilter]
    search_fields = ('=username',)

    @action(methods=['patch', 'get'], detail=False,
            permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        user = self.request.user
        serializer = self.get_serializer(user)
        if self.request.method == 'PATCH':
            serializer = self.get_serializer(
                user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=user.role)
        return Response(serializer.data)


class AccountViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return user.accounts.all()

    def get_serializer_class(self):
        query_params = self.request.query_params.get('currency', '')
        if 'USD' in query_params:
            return AccountUSDSerializer
        if 'EUR' in query_params:
            return AccountEURSerializer
        return AccountSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        account = Account.objects.filter(user=self.request.user)
        if account.exists():
            return Response(
                {'status': f'У вас уже есть счет {account.first().id}'},
                status=status.HTTP_200_OK
            )

        serializer.save(user=self.request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class ActionViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = ActionSerializer
    permission_classes = [permissions.IsAuthenticated]
    ordering_fields = ['date', 'amount']

    def get_queryset(self):
        account = get_object_or_404(Account, user=self.request.user)
        return account.actions.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            account = Account.objects.filter(
                user=self.request.user).get(id=self.request.data['account'])
        except Exception:
            return Response(
                {'account': 'Укажите номер своего счета!'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save(account=account)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ['currency']

    @action(methods=['get'], detail=True,
            permission_classes=[permissions.IsAuthenticated])
    def purchase(self, request, pk):
        service = self.get_object()
        currency_name, currency_rate = CURRENCY_INFO[service.currency]
        if not Account.objects.filter(user=self.request.user).exists():
            return Response(
                {'error': 'Ваш счет не найден!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        user_account = Account.objects.get(user=self.request.user)
        if Transaction.objects.filter(
            account=user_account, service=service
        ).exists():
            return Response(
                {'status': f'У вас уже приобретена услуга {service.name}'},
                status=status.HTTP_200_OK
            )
        service_price = round(
            service.price * decimal.Decimal(currency_rate), 2
        )
        remains_cash = user_account.balance - service_price
        if remains_cash < 0:
            return Response(
                {'status': 'У вас недостаточно средств '
                           f'для покупки {service.name}'},
                status=status.HTTP_402_PAYMENT_REQUIRED
            )
        user_account.balance -= service_price
        user_account.save()
        transaction = Transaction.objects.create(
            account=user_account,
            service=service,
            amount=service_price
        )
        transaction.save()
        return Response(
            {'status': f'Вы успешно купили услугу {service.name}'},
            status=status.HTTP_200_OK
        )


class TransactionViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    ordering_fields = ['date', 'amount']

    def get_queryset(self):
        account = get_object_or_404(Account, user=self.request.user)
        return account.transactions.all()


class TransferViewSet(viewsets.GenericViewSet,
                      mixins.ListModelMixin,
                      mixins.CreateModelMixin):
    serializer_class = TransferSerializer
    permission_classes = [permissions.IsAuthenticated]
    ordering_fields = ['date', 'amount']

    def get_queryset(self):
        account = get_object_or_404(Account, user=self.request.user)
        return account.from_account.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        from_account = Account.objects.filter(
            user=self.request.user
        ).get(id=self.request.data['from_account'])
        amount = self.request.data['amount']
        to_account = Account.objects.get(
            id=self.request.data['to_account']
        )

        remains_cash = from_account.balance - decimal.Decimal(amount)
        if remains_cash < 0:
            return Response(
                {'status': 'У вас недостаточно средств '
                           'для перевода!'},
                status=status.HTTP_402_PAYMENT_REQUIRED
            )

        if from_account == to_account:
            return Response(
                {'error': 'Получатель и отправитель совпадают, '
                          'укажите номер счета получателя!'},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            from_account.balance -= decimal.Decimal(amount)
            from_account.save()

            to_account.balance += decimal.Decimal(amount)
            to_account.save()

            Transfer.objects.create(
                from_account=from_account,
                to_account=to_account,
                amount=amount
            )

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    @action(methods=['get'], detail=False,
            permission_classes=[permissions.IsAuthenticated])
    def to_my_account(self, request):
        account = get_object_or_404(Account, user=self.request.user)
        queryset = account.to_account.all()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        data = self.get_response_data(queryset)
        return Response(data)
