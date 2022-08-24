from django.contrib.auth.models import AbstractUser
from django.db import models

ROLE_CHOICES = [
    ('US', 'user'),
    ('MD', 'moderator'),
    ('AD', 'admin'),
]


class User(AbstractUser):
    bio = models.TextField(verbose_name='Biography', blank=True)
    role = models.CharField(
        max_length=2, verbose_name='Role', choices=ROLE_CHOICES, default='US'
    )
    password = None
    email = models.EmailField()


class ConfirmationData(models.Model):
    confirmation_email = models.EmailField()
    confirmation_username = models.CharField(max_length=19)
    confirmation_code = models.CharField(max_length=8)
