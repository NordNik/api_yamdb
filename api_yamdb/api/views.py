from rest_framework import viewsets, status
from rest_framework import permissions
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from .utils import (
    send_confirmation_mail, get_confirmation_code, get_tokens_for_user
)
from .permissions import (
    SignupPermission, AdminPermission, IsSuperUserPermission
)

from reviews.models import (
    ConfirmationData, User, Genre, Categorie, Title, Comment)
from .serializers import (
    AuthSerializer, TokenSerializer, UserSerializer,
    GenresSerializer, CategoriesSerializer, TitlesSerializer,
    CommentSerializer, MeSerializer)


class GenresViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer
    permission_classes = (permissions.AllowAny,)


class CategoriesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Categorie.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (permissions.AllowAny,)


class TitlesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitlesSerializer
    permission_classes = (permissions.AllowAny,)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = []

    def get_queryset(self):
        return get_object_or_404(Title,
                                 id=self.kwargs.get('post_id')).comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            post=get_object_or_404(Title, id=self.kwargs.get('post_id'))
        )


@api_view(['POST'])
@permission_classes([SignupPermission | IsSuperUserPermission])
def signup(request):
    """
    Sends confirmation mail to mentioned email, and save data about user.

    Whenever user sends post request to signup endpoint the function 
    take username and email, and confirmation code. User data save into 
    ConfirmationData model which being a place of storage of email, username, 
    confirmation code. 
    """
    serializer = AuthSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )
    email = serializer.validated_data['email']
    username = serializer.validated_data['username']
    code = get_confirmation_code()
    ConfirmationData.objects.create(
        confirmation_email=email,
        confirmation_username=username,
        confirmation_code=code
    )
    send_confirmation_mail(email=email, code=code)
    return Response(data=request.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def token(request):
    """Get and send a token to user which has been validated."""
    serializer = TokenSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )
    user = serializer.save()
    token = get_tokens_for_user(user=user)
    return Response(data=token, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    permission_classes = [AdminPermission | IsSuperUserPermission]

    def update(self, request, username=None):
        """Forbid a PUT method."""
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def me(self, request):
        """
        Get or patch information about requested user across users/me endpoint.
        """
        if request.method == 'GET':
            me = get_object_or_404(User, username=request.user.username)
            serializer = MeSerializer(me)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = MeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
               data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
