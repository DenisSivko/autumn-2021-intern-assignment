from django.contrib import admin

from .models import Account, Action, Service, Transaction, Transfer, User

EMPTY_VALUE = '-пусто-'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'bio', 'role')
    search_fields = ('username',)
    list_filter = ('role',)
    empty_value_display = EMPTY_VALUE


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'balance', 'user')
    search_fields = ('user',)
    list_filter = ('user', 'balance')
    empty_value_display = EMPTY_VALUE


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'date', 'account')
    search_fields = ('account',)
    list_filter = ('date', 'account')
    empty_value_display = EMPTY_VALUE


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'price', 'currency')
    search_fields = ('name',)
    list_filter = ('name', 'currency')
    empty_value_display = EMPTY_VALUE


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'account', 'service')
    search_fields = ('account', 'service')
    list_filter = ('date', 'service')
    empty_value_display = EMPTY_VALUE


@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    list_display = ('id', 'from_account', 'to_account', 'amount', 'date')
    search_fields = ('from_account', 'to_account')
    list_filter = ('date', 'from_account', 'to_account')
    empty_value_display = EMPTY_VALUE
