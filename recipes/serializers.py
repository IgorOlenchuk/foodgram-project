from rest_framework import serializers
from .models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('text', 'author', 'pub_date')
        model = Recipe
