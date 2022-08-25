from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.generics import get_object_or_404

from reviews.models import Genres, Categories, Titles, Comment
from .serializers import (
    GenresSerializer, CategoriesSerializer, TitlesSerializer,
    CommentSerializer)


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


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = []

    def get_queryset(self):
        return get_object_or_404(Titles,
                                 id=self.kwargs.get('post_id')).comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            post=get_object_or_404(Titles, id=self.kwargs.get('post_id'))
        )
