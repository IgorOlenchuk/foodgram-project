from django.db import models

from recipes.models import Favorite, Purchase
from users.models import Subscription


class RecipeManager(models.Manager):
    def tag_filter(self, tags):
        if tags:
            return super().get_queryset().prefetch_related(
                'author', 'tags'
            ).filter(
                tags__slug__in=tags
            ).distinct()
        else:
            return super().get_queryset().prefetch_related(
                'author', 'tags'
            ).all()


def extend_context(context, user):
    context['purchase_list'] = Purchase.purchase.get_purchases_list(user)
    context['favorites'] = Favorite.favorite.get_favorites(user)
    return context


def add_subscription_status(context, user, author):
    context['is_subscribed'] = Subscription.objects.filter(
        user=user, author=author
    ).exists()
    return context
