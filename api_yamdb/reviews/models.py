from django.contrib.auth.models import AbstractUser
from django.db.models import TextField, CharField, EmailField

ROLE_CHOICES = [
    ('US', 'user'),
    ('MD', 'moderator'),
    ('AD', 'admin'),
    ]


class User(AbstractUser):
    bio = TextField(verbose_name='Biography', blank=True)
    role = CharField(
        max_length=2, verbose_name='Role', choices=ROLE_CHOICES, default='US'
    )
    password = None
    email = EmailField()
