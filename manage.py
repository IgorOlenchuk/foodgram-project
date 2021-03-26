import os
import sys

from django.db import models

from recipes.views import Favorite, Purchase, Subscription


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodgram.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


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


if __name__ == '__main__':
    main()
