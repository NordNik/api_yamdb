from reviews.models import Title, Review
from .serializers import CommentSerializer, ReviewSerializer
from .permissions import StaffOrAuthorOrReadOnly

from rest_framework.generics import get_object_or_404
from rest_framework import viewsets


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (StaffOrAuthorOrReadOnly,)

    def get_queryset(self):
        return get_object_or_404(Review,
                                 id=self.kwargs.get('review_id')).comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=get_object_or_404(Review, id=self.kwargs.get('post_id'))
        )


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (StaffOrAuthorOrReadOnly,)

    def get_queryset(self):
        return get_object_or_404(Title,
                                 id=self.kwargs.get('title_id')).reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=get_object_or_404(Title, id=self.kwargs.get('title_id'))
        )
