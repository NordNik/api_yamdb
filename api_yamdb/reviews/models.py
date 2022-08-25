from django.contrib.auth.models import AbstractUser
from django.db import models


ROLE_CHOICES = [
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Админ'),
]


class User(AbstractUser):
    bio = models.TextField(verbose_name='Biography', blank=True)
    role = models.CharField(
        max_length=2, verbose_name='Role', choices=ROLE_CHOICES, default='user'
    )
    password = models.CharField(max_length=20, null=True)
    email = models.EmailField(unique=True)


class ConfirmationData(models.Model):
    confirmation_email = models.EmailField()
    confirmation_username = models.CharField(max_length=19)
    confirmation_code = models.CharField(max_length=8)
