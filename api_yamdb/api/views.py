from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import permissions
from rest_framework import filters
from django.shortcuts import get_object_or_404
from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin, RetrieveModelMixin)

from reviews.models import Genres
from .serializers import GenresSerializer


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    permission_classes = (permissions.AllowAny,)
