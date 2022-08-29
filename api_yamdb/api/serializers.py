from rest_framework import serializers
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError

from reviews.models import (User, Categorie, Genre, Title, Comment)
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
        lookup_field = 'slug'
        model = Categorie


class TitlesSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug', read_only=False,
        queryset=Genre.objects.all(),
        many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', read_only=False,
        queryset=Categorie.objects.all()
    )

    class Meta:
        fields = (
            'id', 'name', 'year', 'genre', 'category', 'description'
        )
        model = Title


class ReviewsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    review = serializers.SlugRelatedField(
        read_only=True, slug_field='text'
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


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    def validate_score(self, value):
        if 0 > value > 10:
            raise serializers.ValidationError('Оценка по 10-бальной шкале!')
        return value

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if (
            request.method == 'POST'
            and Review.objects.filter(title=title, author=author).exists()
        ):
            raise ValidationError('Можно оставить только один отзыв')
        return data

    class Meta:
        fields = '__all__'
        model = Review


class MeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        read_only_fields = ('role', 'username', 'email')
