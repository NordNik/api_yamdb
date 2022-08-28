from django.contrib.auth.models import AbstractUser
from django.db import models


ROLE_CHOICES = [
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Админ'),
    ('anon', 'Аноним'),
]


class User(AbstractUser):
    bio = models.TextField(verbose_name='Biography', blank=True)
    role = models.CharField(
        max_length=9, verbose_name='Role',
        choices=ROLE_CHOICES, default='user'
    )
    password = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(unique=True)


class ConfirmationData(models.Model):
    confirmation_email = models.EmailField()
    confirmation_username = models.CharField(max_length=19)
    confirmation_code = models.CharField(max_length=8, )


class Categorie(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.TextField()
    category = models.ForeignKey(
        Categorie, on_delete=models.SET_NULL,
        related_name='titles', blank=False, null=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        blank=True,
    )
    year = models.PositiveSmallIntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )


class Vote(models.Model):
    value = models.SmallIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Title, on_delete=models.CASCADE)
    voted_on = models.DateTimeField(auto_now=True)

    class Meta:
        # эта команда не даст повторно голосовать
        unique_together = ('user', 'post')
