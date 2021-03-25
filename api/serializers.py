from rest_framework.serializers import ModelSerializer
from rest_framework.fields import HiddenField, CurrentUserDefault
from rest_framework.exceptions import ValidationError

from .models import Favorite, Purchase, Subscription
from recipes.models import Ingredient


def validate_author(data):
    if data.get('author') == data.get('user'):
        raise ValidationError('Нельзя подписаться на самого себя')
    return data


class IngredientSerializer(ModelSerializer):
    class Meta:
        fields = ('title', 'dimension')
        model = Ingredient


class SubscriptionSerializer(CurrentUserDefault, ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        fields = ('author', 'user')
        model = Subscription
        validators = (validate_author, )


class FavoriteSerializer(CurrentUserDefault, ModelSerializer):
    class Meta:
        fields = ('recipe',)
        model = Favorite


class PurchaseSerializer(CurrentUserDefault, ModelSerializer):
    class Meta:
        fields = ('recipe',)
        model = Purchase
