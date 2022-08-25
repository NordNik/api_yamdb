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


class Categories(models.Model):
    category_name = models.CharField(max_length=200)
    category_slug = models.SlugField(unique=True)

    def __str__(self):
        return self.category_name


class Genres(models.Model):
    genre_name = models.CharField(max_length=200)
    genre_slug = models.SlugField(unique=True)

    def __str__(self):
        return self.genre_name


class Titles(models.Model):
    title_name = models.TextField()
    category = models.ForeignKey(
        Categories, on_delete=models.CASCADE,
        related_name='titles', blank=False, null=False
    )
    genre = models.ForeignKey(
        Genres, on_delete=models.CASCADE,
        related_name='titles', blank=False, null=False
    )

    def __str__(self):
        return self.name


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)


class Vote(models.Model):
    value = models.SmallIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    voted_on = models.DateTimeField(auto_now=True)

    class Meta:
        # эта команда не даст повторно голосовать
        unique_together = ('user', 'post')
