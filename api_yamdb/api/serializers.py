from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from reviews.models import (User, Categorie, Genre, Title, Comment)
from .utils import get_confirmation_code, send_confirmation_mail


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Genre


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Categorie


class TitlesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
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
        """
        Forbide a 'me' username and delete old confirmation data if it exists.
        """
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
        read_only_fields = ('role',)
