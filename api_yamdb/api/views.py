from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions

from reviews.models import ConfirmationData, User, Genres
from .serializers import (
    AuthSerializer, TokenSerializer, UserSerializer, GenresSerializer
)
from .utils import (
    send_confirmation_mail, get_confirmation_code, get_tokens_for_user
)
from .permissions import (
    SignupPermission, AdminPermission, IsSuperUserPermission
)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    permission_classes = (permissions.AllowAny,)


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
