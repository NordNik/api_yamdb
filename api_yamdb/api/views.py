from rest_framework import viewsets
from rest_framework import permissions

from reviews.models import Genres, Categories, Titles
from .serializers import (
    GenresSerializer, CategoriesSerializer, TitlesSerializer)


class GenresViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    permission_classes = (permissions.AllowAny,)


class CategoriesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (permissions.AllowAny,)


class TitlesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    permission_classes = (permissions.AllowAny,)
