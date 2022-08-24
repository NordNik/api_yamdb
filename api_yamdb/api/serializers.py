from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from reviews.models import User, ConfirmationData
from django.shortcuts import get_object_or_404


class AuthSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']

    def validate(self, data):
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

    def validate(self, data):
        instance = ConfirmationData.objects.filter(
            confirmation_code=data['confirmation_code'],
            confirmation_username=data['confirmation_username'],
        )
        if not instance.exists():
            raise serializers.ValidationError("Code or username is'not valid")
        return data

    def create(self, validated_data):
        user = get_object_or_404(
            ConfirmationData,
            confirmation_username=validated_data['confirmation_username']
        )
        return User.objects.create_user(
            email=user.confirmation_email,
            username=user.confirmation_username
        )
