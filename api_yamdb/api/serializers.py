from rest_framework import serializers
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions

from reviews.models import (User, Categorie, Genre, Title, Comment, GenreTitle)
from .utils import get_confirmation_code, send_confirmation_mail


def auth_client(user):
    refresh = RefreshToken.for_user(user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client


class GenresSerializer(serializers.ModelSerializer):

    def validate(self, data):
        if not self.context['request'].user.is_authenticated:
            raise ValidationError(
                "You do not have permission for this action")
        if self.context['request'].user.role != 'admin':
            raise ValidationError(
                "You do not have permission for this action")
        return data

    class Meta:
        fields = (
            'name', 'slug',
        )
        model = Genre
        lookup_field = 'slug'


class CategoriesSerializer(serializers.ModelSerializer):

    def validate(self, data):
        if not self.context['request'].user.is_authenticated:
            raise ValidationError(
                "You do not have permission for this action")
        if self.context['request'].user.role != 'admin':
            raise ValidationError(
                "You do not have permission for this action")
        return data

    class Meta:
        fields = (
            'name', 'slug',
        )
        model = Categorie
        lookup_field = 'slug'


class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenresSerializer(many=True,)
    category = CategoriesSerializer()

    class Meta:
        fields = (
            'id', 'name', 'year', 'genre', 'category', 'description'
        )
        model = Title


class TitlesPOSTSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True,
        queryset=Genre.objects.all())
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Categorie.objects.all())

    class Meta:
        fields = (
            'id', 'name', 'year', 'genre', 'category', 'description'
        )
        model = Title


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment


class AuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')

    def validate(self, data):
        """Forbide a 'me' username."""
        if data['username'].lower() == 'me':
            raise serializers.ValidationError("You can't use 'me' as username")
        return data

    def create(self, validated_data):
        """
        Generate code and send it to mentioned email and create user.
        """
        email = validated_data['email']
        username = validated_data['username']
        code = get_confirmation_code()
        send_confirmation_mail(email=email, code=code)
        return User.objects.create_user(
            email=email,
            username=username,
            confirmation_code=code
        )


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=8)

    def validate_confirmation_code(self, value):
        if len(value) != 8:
            raise serializers.ValidationError(
                "Code must be 8 characters long "
            )
        return value

    def validate_username(self, value):
        """Check if user exists, if not raised 404 error"""
        get_object_or_404(User, username=value)
        return value


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class MeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        read_only_fields = ('role', 'username', 'email')
