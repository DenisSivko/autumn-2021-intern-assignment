from django.core.exceptions import ValidationError


def validate_price(price):
    if price < 1:
        raise ValidationError('Услуга не может быть бесплатной!')
