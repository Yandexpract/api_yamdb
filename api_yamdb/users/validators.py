import re

from rest_framework.exceptions import ValidationError

from users.models import User


def validate_username(value):
    if User.objects.filter(username=value).exists():
        raise ValidationError('Пользователь с таким именем '
                              'уже зарегестрирован')

    if value == 'me':
        raise ValidationError(
            'me нельзя использовать в качестве имени',
        )
    if not re.fullmatch(r'^[\w.@+-]+\Z', value):
        raise ValidationError(
            'Имя пользователя не соотвествует формату',
        )
    return value


def validate_email(value):
    if User.objects.filter(email=value).exists():
        raise ValidationError('Пользователь с такой почтой '
                              'уже зарегестрирован')
