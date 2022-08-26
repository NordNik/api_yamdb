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


class ConfirmationData(models.Model):
    confirmation_email = models. EmailField()
    confirmation_username = models.CharField(max_length=19)
    confirmation_code = models. CharField(max_length=8)


class Categorie(models.Model):
    categorie_name = models.CharField(max_length=200)
    categorie_slug = models.SlugField(unique=True)

    def __str__(self):
        return self.categorie_name


class Genre(models.Model):
    genre_name = models.CharField(max_length=200)
    genre_slug = models.SlugField(unique=True)

    def __str__(self):
        return self.genre_name


class Title(models.Model):
    title_name = models.TextField()
    categorie = models.ForeignKey(
        Categorie, on_delete=models.CASCADE,
        related_name='titles', blank=False, null=False
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles'
    )

    def __str__(self):
        return self.title_name


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)


class Vote(models.Model):
    value = models.SmallIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    voted_on = models.DateTimeField(auto_now=True)

    class Meta:
        # эта команда не даст повторно голосовать
        unique_together = ('user', 'title')


class Reviews(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
)
