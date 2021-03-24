from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import UniqueConstraint

from recipes.models import Recipe

User = get_user_model()


class Subscription(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follower',
        verbose_name='Избранный автор',
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,  related_name='following',
        verbose_name='Подписчик',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'], name='unique_subscription'
            )
        ]


class Favorite(models.Model):

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='favorites',
        verbose_name='Пользователь',
    )
    recipes = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='favored_by',
        verbose_name='Избранный рецепт',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipes'], name='unique_favorite'
            )
        ]


class Purchase(models.Model):

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='purchases',
        verbose_name='Пользователь',
    )
    recipes = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name='Рецепт в покупках',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipes'], name='unique_purchase'
            )
        ]
