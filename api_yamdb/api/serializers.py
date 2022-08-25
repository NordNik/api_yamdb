from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from reviews.models import User, ConfirmationData
from django.shortcuts import get_object_or_404


class AuthSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    email = serializers.EmailField(required=True)

    def validate(self, data):
        if data['username'].lower() == 'me':
            raise serializers.ValidationError("You can't use 'me' as username")
        instance = ConfirmationData.objects.filter(
            confirmation_email=data['email'],
            confirmation_username=data['username'],
        )
        if instance.exists():
            instance.delete()
        return data


class TokenSerializer(ModelSerializer):
    username = serializers.CharField(source='confirmation_username')

    class Meta:
        model = ConfirmationData
        fields = ['username', 'confirmation_code']

    def create(self, validated_data):
        user_data = get_object_or_404(
            ConfirmationData,
            confirmation_username=validated_data['confirmation_username'],
            confirmation_code=validated_data['confirmation_code']
        )
        user = User.objects.filter(username=user_data.confirmation_username)
        if user.exists():
            return user.get()
        return User.objects.create_user(
            email=user_data.confirmation_email,
            username=user_data.confirmation_username
        )


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        ]
