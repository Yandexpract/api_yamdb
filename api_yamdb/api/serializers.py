from django.core.validators import MaxLengthValidator, RegexValidator

from rest_framework import serializers
from users.models import User
from users.validators import validate_username, validate_email


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('first_name', 'last_name', 'username',
                  'bio', 'email', 'role')
        model = User
        read_only_field = ('role')


class AuthSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        max_length=254,
        validators=(RegexValidator(r'^[\w.+-]+\Z'),
                    validate_email))

    username = serializers.CharField(
        required=True, max_length=150,
        validators=(
            MaxLengthValidator(150),
            RegexValidator(r'^[\w.@+-]+\Z'),
            validate_username,))

    class Meta:
        model = User
        fields = ('email', 'username')


class GetTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')
