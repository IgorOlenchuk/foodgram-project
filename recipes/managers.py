from recipes.models import Purchase, Favorite
from users.models import Subscription


def extend_context(context, user):
    context['purchase_list'] = Purchase.purchase.get_purchases_list(user)
    context['favorites'] = Favorite.favorite.get_favorites(user)
    return context


def add_subscription_status(context, user, author):
    context['is_subscribed'] = Subscription.objects.filter(
        user=user, author=author
    ).exists()
    return context
