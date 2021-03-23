from rest_framework import serializers
from rest_framework.fields import HiddenField, CurrentUserDefault
from rest_framework.exceptions import ValidationError

from .models import Favorite, Purchase, Subscription
from recipes.models import Ingredient


def validate_author(data):
    if data.get('author') == data.get('user'):
        raise ValidationError('Нельзя подписаться на самого себя')
    return data


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('title', 'dimension')
        model = Ingredient


class SubscriptionSerializer(CurrentUserDefault, serializers.ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        fields = ('author', 'user')
        model = Subscription
        validators = (validate_author, )


class FavoriteSerializer(CurrentUserDefault, serializers.ModelSerializer):
    class Meta:
        fields = ('recipe',)
        model = Favorite


class PurchaseSerializer(CurrentUserDefault, serializers.ModelSerializer):
    class Meta:
        fields = ('recipe',)
        model = Purchase
