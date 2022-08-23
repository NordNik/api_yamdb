from tkinter import CASCADE
from unicodedata import category
from django.db import models


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
        Genres, on_delete=CASCADE,
        related_name='titles', blank=False, null=False
    )

    def __str__(self):
        return self.name
