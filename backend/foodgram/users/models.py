from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователя с выбором его роли."""
    ADMIN = 'admin'
    USER = 'user'

    ROLES = [
        (ADMIN, 'Администратор'),
        (USER, 'Пользователь'),
    ]

    username = models.CharField(
        verbose_name='Никнейм',
        max_length=30,
        unique=True,
    )
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=255,
        unique=True,
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=30,
        choices=ROLES,
        default=USER,
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=20,
        null=True,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=40,
        null=True,
    )

    @property
    def is_admin(self):
        """Пользователь в статусе администратора."""
        return self.role == self.ADMIN

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    class Meta:
        ordering = ['id']
