from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователя с выбором его роли."""
    first_name = models.CharField(
        verbose_name='name',
        max_length=150,
    )
    last_name = models.CharField(
        verbose_name='last name',
        max_length=150,
    )
    email = models.EmailField(
        verbose_name='email',
        max_length=254,
        unique=True,
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ('first_name', 'last_name', 'email',)

    class Meta:
        ordering = ['id']
