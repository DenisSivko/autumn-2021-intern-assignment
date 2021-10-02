import decimal

from rest_framework import serializers

from .models import Account, Action, Service, Transaction, Transfer, User

USD_RATE = 72.56
EURO_RATE = 85.46
RUB_RATE = 1


class AccountSerializer(serializers.ModelSerializer):
    actions = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    currency = serializers.CharField(default='RUB', read_only=True)

    class Meta:
        model = Account
        fields = ('id', 'balance', 'currency', 'actions')
        read_only_fields = ('id', 'balance', 'currency', 'actions')


class AccountUSDSerializer(serializers.ModelSerializer):
    actions = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    currency = serializers.CharField(default='USD', read_only=True)
    balance = serializers.SerializerMethodField(
        method_name='currency_conversion'
    )

    class Meta:
        model = Account
        fields = ('id', 'balance', 'currency', 'actions')
        read_only_fields = ('id', 'balance', 'currency', 'actions')

    def currency_conversion(self, obj):
        request = self.context.get('request')
        user_account = Account.objects.filter(user=request.user).first()
        balance = round(user_account.balance / decimal.Decimal(USD_RATE), 2)
        return balance


class AccountEURSerializer(serializers.ModelSerializer):
    actions = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    currency = serializers.CharField(default='EUR', read_only=True)
    balance = serializers.SerializerMethodField(
        method_name='currency_conversion'
    )

    class Meta:
        model = Account
        fields = ('id', 'balance', 'currency', 'actions')
        read_only_fields = ('id', 'balance', 'currency', 'actions')

    def currency_conversion(self, obj):
        request = self.context.get('request')
        user_account = Account.objects.filter(user=request.user).first()
        balance = round(user_account.balance / decimal.Decimal(EURO_RATE), 2)
        return balance


class ActionSerializer(serializers.ModelSerializer):
    currency = serializers.CharField(default='RUB', read_only=True)

    class Meta:
        model = Action
        fields = ('id', 'account', 'amount', 'currency', 'date')
        read_only_fields = ('id', 'date', 'currency')

    def create(self, validated_data):
        validated_data['account'].balance += validated_data['amount']
        validated_data['account'].save()
        return super().create(validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'first_name', 'last_name', 'username', 'bio', 'email', 'role'
        )
        model = User
        read_only_field = ('role',)


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = (
            'id', 'name', 'description', 'price', 'currency'
        )


class TransactionSerializer(serializers.ModelSerializer):
    currency = serializers.CharField(default='RUB', read_only=True)

    class Meta:
        model = Transaction
        fields = ('id', 'date', 'account', 'service', 'amount', 'currency')


class TransferSerializer(serializers.ModelSerializer):
    currency = serializers.CharField(default='RUB', read_only=True)

    class Meta:
        model = Transfer
        fields = (
            'id', 'from_account', 'to_account', 'amount', 'currency', 'date'
        )


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class TokenSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    confirmation_code = serializers.CharField(required=True)
