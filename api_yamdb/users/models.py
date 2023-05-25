from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_USER = 'user'
    ROLE_MODERATOR = 'moderator'
    ROLE_ADMIN = 'admin'
    ROLE_CHOICES = (
        (ROLE_USER, 'user'),
        (ROLE_MODERATOR, 'moderator'),
        (ROLE_ADMIN, 'admin'))

    username = models.TextField(
        max_length=150,
        unique=True,
        verbose_name='Имя пользователя',
        help_text='Укажите имя пользователя')

    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Электронная почта',
        help_text='Укажите электронную почту')

    bio = models.TextField('Биография', blank=True,)
    role = models.CharField('Роль', max_length=20,
                            choices=ROLE_CHOICES, default='user')

    @property
    def is_admin(self):
        return (self.role == self.ROLE_ADMIN
                or self.is_superuser
                or self.is_staff)

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR
