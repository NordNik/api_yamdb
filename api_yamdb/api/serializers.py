from rest_framework import serializers
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

from reviews.models import (User, Categorie, Genre, Title, Comment, Review)
from .utils import get_confirmation_code, send_confirmation_mail


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
        exclude = ('id', )
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
        exclude = ('id', )
        model = Categorie
        lookup_field = 'slug'


class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenresSerializer(many=True,)
    category = CategoriesSerializer()

    class Meta:
        fields = (
            'id', 'name', 'year', 'genre', 'category', 'description', 'rating'
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
            'id', 'name', 'year', 'genre', 'category', 'description', 'rating'
        )
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    score = serializers.IntegerField(
        validators=(
            MinValueValidator(1),
            MaxValueValidator(10)
        )
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review


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


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    review = serializers.CharField(read_only=True)

    class Meta:
        fields = ('id', 'author', 'text', 'pub_date', 'review')
        model = Comment


class MeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        read_only_fields = ('role', 'username', 'email')
