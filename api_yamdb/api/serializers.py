from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

from reviews.models import (User, Categorie, Genre, Title, Comment, Review)


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


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class MeSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        read_only_fields = ('role', 'username', 'email')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    review = serializers.CharField(read_only=True)

    class Meta:
        fields = ('id', 'author', 'text', 'pub_date', 'review')
        model = Comment
