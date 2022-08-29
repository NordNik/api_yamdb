from rest_framework import viewsets, status, permissions, filters
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import (
    api_view, permission_classes, action, throttle_classes)
from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin,
    UpdateModelMixin, DestroyModelMixin)
from rest_framework import filters
from .utils import get_tokens_for_user

from .permissions import (
    SignupPermission, AdminPermission,
    IsSuperUserPermission, AdminOrReadOnly,
    StaffOrAuthorOrReadOnly
)

from reviews.models import (
    User, Genre, Categorie, Title, Comment, Review)
from .serializers import (
    AuthSerializer, TokenSerializer, UserSerializer,
    GenresSerializer, CategoriesSerializer, TitlesSerializer,
    CommentSerializer, MeSerializer, ReviewSerializer)
from .throttles import NoGuessRateThrottle


class GenresViewSet(CreateModelMixin, ListModelMixin,
                    DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer
    permission_classes = (AdminOrReadOnly, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoriesViewSet(CreateModelMixin, ListModelMixin,
                        DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Categorie.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (AdminOrReadOnly, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)
    lookup_field = 'slug'


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitlesSerializer
    permission_classes = (AdminOrReadOnly, )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (StaffOrAuthorOrReadOnly,)

    def get_queryset(self):
        return get_object_or_404(
            Review, id=self.kwargs.get('review_id')
        ).comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=get_object_or_404(Review, id=self.kwargs.get('review_id'))
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


@api_view(['POST'])
@permission_classes([SignupPermission | IsSuperUserPermission])
def signup(request):
    """
    Sends confirmation mail to mentioned email, and save data about user.
    """
    serializer = AuthSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )
    serializer.save()
    return Response(data=request.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
@throttle_classes([NoGuessRateThrottle])
def token(request):
    """Get and send a token to user which has been validated."""
    serializer = TokenSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )
    user = get_object_or_404(
        User,
        username=serializer.validated_data['username'],
        confirmation_code=serializer.validated_data['confirmation_code']
    )
    token = get_tokens_for_user(user=user)
    return Response(data=token, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AdminPermission | IsSuperUserPermission,)
    http_method_names = ('get', 'post', 'patch', 'delete')
    search_fields = ('username',)

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def me(self, request):
        """
        Get or update (patch method) inf about requested user.
        """
        me = get_object_or_404(User, username=request.user.username)
        if request.method == 'GET':
            serializer = MeSerializer(me)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            serializer = MeSerializer(me, data=request.data)
            if not serializer.is_valid():
                return Response(
                    data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
