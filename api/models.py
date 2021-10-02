from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_price


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER_ROLE = [
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    ]

    email = models.EmailField('Почта пользователя', unique=True)
    bio = models.TextField('О себе', blank=True, max_length=200)
    role = models.CharField(
        'Роль пользователя', max_length=50,
        choices=USER_ROLE, default=USER
    )

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_staff

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Account(models.Model):
    balance = models.DecimalField(
        'Баланс', default=0,
        max_digits=12, decimal_places=2
    )
    user = models.ForeignKey(
        User, on_delete=models.PROTECT,
        related_name='accounts', verbose_name='Пользователь'
    )

    class Meta:
        ordering = ('user',)
        verbose_name = 'Счет'
        verbose_name_plural = 'Счета'

    def __str__(self):
        return f'{self.id} - {self.user.username} - {self.balance}'


class Action(models.Model):
    amount = models.DecimalField(
        'Сумма', max_digits=12, decimal_places=2
    )
    date = models.DateTimeField('Дата пополнения счета', auto_now_add=True)
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE,
        related_name='actions', verbose_name='Счет'
    )

    class Meta:
        ordering = ('date',)
        verbose_name = 'Пополнение'
        verbose_name_plural = 'Пополнения'

    def __str__(self):
        return (
            f'Счет номер {self.account.id} '
            f'был пополнен на {self.amount} руб.'
        )


class Service(models.Model):
    RUB = 'RUB'
    USD = 'USD'
    EUR = 'EUR'
    CUREENCY = [
        (RUB, 'RUB'),
        (USD, 'USD'),
        (EUR, 'EUR'),
    ]

    name = models.CharField('Название услуги', max_length=50)
    description = models.TextField('Описание услуги')
    price = models.DecimalField(
        'Цена услуги', max_digits=12,
        decimal_places=2, validators=[validate_price]
    )
    currency = models.CharField(
        'Валюта', choices=CUREENCY,
        default='RUB', max_length=10
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    def __str__(self):
        return self.name


class Transaction(models.Model):
    date = models.DateTimeField('Дата приобретения услуги', auto_now_add=True)
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE,
        related_name='transactions', verbose_name='Счет'
    )
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE,
        related_name='transactions', verbose_name='Услуга'
    )
    amount = models.DecimalField(
        'Сумма', max_digits=12, decimal_places=2
    )

    class Meta:
        ordering = ('date',)
        verbose_name = 'Приобретение'
        verbose_name_plural = 'Приобретения'

    def __str__(self):
        return (
            f'Счет номер {self.account.id} '
            f'приобрел услугу {self.service.name} '
            f'за {self.service.price} {self.service.currency}'
        )


class Transfer(models.Model):
    from_account = models.ForeignKey(
        Account, on_delete=models.CASCADE,
        related_name='from_account', verbose_name='Счет отправителя'
    )
    to_account = models.ForeignKey(
        Account, on_delete=models.CASCADE,
        related_name='to_account', verbose_name='Счет получателя'
    )
    amount = models.DecimalField(
        'Сумма', max_digits=12, decimal_places=2
    )
    date = models.DateTimeField(
        'Дата перевода денежных средств', auto_now_add=True
    )

    class Meta:
        ordering = ('date',)
        verbose_name = 'Перевод денежных средств'
        verbose_name_plural = 'Переводы денежных средств'

    def __str__(self):
        return (
            f'Перевод с {self.from_account} на {self.to_account}, '
            f'сумма перевода {self.amount}'
        )
