from recipes.models import Purchase


def counter(request):
    user = request.user
    counter = Purchase.recipe.counter(
        user) if user.is_authenticated else None
    return {
        'counter': counter,
    }
