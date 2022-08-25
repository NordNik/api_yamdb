from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Categories, Genres, Titles, User


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Genres
