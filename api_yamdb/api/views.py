from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.decorators import api_view

from reviews.models import ConfirmationData
from .serializers import AuthSerializer, TokenSerializer
from .utils import (
    send_confirmation_mail, get_confirmation_code, get_tokens_for_user
    )


@api_view(['POST'])
def signup(request):
    serializer = AuthSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)
    email = serializer.validated_data['email']
    username = serializer.validated_data['username']
    code = get_confirmation_code()
    ConfirmationData.objects.create(
        confirmation_email=email,
        confirmation_username=username,
        confirmation_code=code
    )
    send_confirmation_mail(email=email, code=code)
    return Response(data=request.data, status=HTTP_200_OK)


@api_view(['POST'])
def token(request):
    serializer = TokenSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)
    user = serializer.save()
    token = get_tokens_for_user(user=user)
    return Response(data=token, status=HTTP_200_OK)
