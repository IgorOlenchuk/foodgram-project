import json
from urllib.parse import unquote

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.http import (require_GET, require_http_methods,
                                          require_POST)

from users.models import Subscription

from .forms import RecipeForm
from .managers import add_subscription_status, extend_context, Favorite, Purchase
from .models import Ingredient, Product, Recipe, Tag, User


@require_GET
def index(request):
    paginator = Paginator(settings.PAGINATION_PAGE_SIZE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'all_tags': Tag.objects.all(),
        'page': page,
        'paginator': paginator
    }
    user = request.user
    if user.is_authenticated:
        context['active'] = 'recipe'
        extend_context(context, user)
    return render(request, 'index.html', context)


@require_GET
def profile(request, user_id):
    profile = get_object_or_404(User, id=user_id)
    tags = request.GET.getlist('tag')
    recipes_list = Recipe.recipes.tag_filter(tags)
    paginator = Paginator(
        recipes_list.filter(author=profile),
        settings.PAGINATION_PAGE_SIZE
    )
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'all_tags': Tag.objects.all(),
        'profile': profile,
        'page': page,
        'paginator': paginator
    }
    # Если юзер авторизован, добавляет в контекст список
    # покупок и избранное
    user = request.user
    if user.is_authenticated:
        add_subscription_status(context, user, profile)
        extend_context(context, user)
    return render(request, 'profile.html', context)


@require_GET
def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    context = {
        'recipe': recipe,
    }
    user = request.user
    if user.is_authenticated:
        add_subscription_status(context, user, recipe.author)
        extend_context(context, user)
    return render(request, 'recipe_detail.html', context)


class FavoriteView(View):
    model = Favorite

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        tags = self.request.GET.getlist('tag')
        user = self.request.user
        queryset = self.model.favorite.get_tag_filtered(user, tags)
        return queryset

    def get(self, request):
        paginator = Paginator(
            self.get_queryset(),
            settings.PAGINATION_PAGE_SIZE
        )
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        purchase_list = Purchase.purchase.get_purchases_list(request.user)
        context = {
            'all_tags': Tag.objects.all(),
            'purchase_list': purchase_list,
            'active': 'favorite',
            'paginator': paginator,
            'page': page
        }
        return render(request, 'favorites.html', context)

    def post(self, request):
        json_data = json.loads(request.body.decode())
        recipe_id = []
        if json_data['id'] is True:
            try:
                recipe_id = json_data['id']
            except KeyError:
                recipe_id = None
        recipe = get_object_or_404(Recipe, id=recipe_id)
        data = {'success': True}
        favorite = Favorite.favorite.get_user(request.user)
        is_favorite = favorite.recipes.filter(id=recipe_id).exists()
        if is_favorite:
            data['success'] = False
        else:
            favorite.recipes.add(recipe)
        return JsonResponse(data)


@login_required(login_url='auth/login/')
@require_http_methods('DELETE')
def delete_favorite(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    data = {'success': True}
    try:
        favorite = Favorite.favorite.get(user=request.user)
    except User.DoesNotExist:
        data['success'] = False
    if not favorite.recipes.filter(id=recipe_id).exists():
        data['success'] = False
    favorite.recipes.remove(recipe)
    return JsonResponse(data)


@login_required(login_url='auth/login/')
@require_GET
def get_subscriptions(request):
    try:
        subscriptions = Subscription.objects.filter(
            user=request.user
        ).order_by('pk')
    except User.DoesNotExist:
        subscriptions = []
    page_num = request.GET.get('page')
    paginator = Paginator(
        subscriptions,
        settings.PAGINATION_PAGE_SIZE)
    page = paginator.get_page(page_num)
    context = {
        'active': 'subscription',
        'paginator': paginator,
        'page': page,
    }
    return render(request, 'subscriptions.html', context)


@login_required(login_url='auth/login/')
@require_POST
def subscription(request):
    json_data = json.loads(request.body.decode())
    author = get_object_or_404(User, id=json_data['id'])
    is_exist = Subscription.objects.filter(
        user=request.user, author=author).exists()
    data = {'success': True}
    if is_exist:
        data['success'] = False
    else:
        Subscription.objects.create(user=request.user, author=author)
    return JsonResponse(data)


@login_required(login_url='auth/login/')
@require_http_methods('DELETE')
def delete_subscription(request, author_id):
    author = get_object_or_404(User, id=author_id)
    data = {'success': True}
    follow = Subscription.objects.filter(
        user=request.user, author=author)
    if not follow:
        data['success'] = False
    follow.delete()
    return JsonResponse(data)


class PurchaseView(View):
    model = Purchase

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        queryset = self.model.purchase.get_purchases_list(self.request.user)
        return queryset

    def get(self, request):
        recipes_list = self.get_queryset()
        context = {
            'recipes_list': recipes_list,
            'active': 'purchase'
        }
        return render(request, 'purchases.html', context)

    def post(self, request):
        json_data = json.loads(request.body.decode())
        recipe_id = json_data['id']
        recipe = get_object_or_404(Recipe, id=recipe_id)
        purchase = Purchase.purchase.get_user_purchase(user=request.user)
        data = {
            'success': True
        }
        if not purchase.recipes.filter(id=recipe_id).exists():
            purchase.recipes.add(recipe)
            return JsonResponse(data)
        data['success'] = False
        return JsonResponse(data)


@login_required(login_url='auth/login/')
@require_http_methods('DELETE')
def delete_purchase(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    data = {
        'success': True
    }
    try:
        purchase = Purchase.purchase.get(user=request.user)
    except User.DoesNotExist:
        data['success'] = False
    if not purchase.recipes.filter(id=recipe_id).exists():
        data['success'] = False
    purchase.recipes.remove(recipe)
    return JsonResponse(data)


@login_required(login_url='auth/login/')
@require_GET
def send_shop_list(request):
    user = request.user
    ingredients = Ingredient.objects.select_related(
        'ingredient'
    ).filter(
        recipe__purchase__user=user
    ).values(
        'ingredient__title', 'ingredient__unit'
    ).annotate(total=Sum('amount'))
    filename = f'{user.username}_list.txt'
    products = [
        (f'+ {i["ingredient__title"]} ({i["ingredient__unit"]}) -'
         f' {i["total"]}')
        for i in ingredients]
    content = '  Продукт (единицы) - количество \n \n' + '\n'.join(products)
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response


@login_required(login_url='auth/login/')
def new_recipe(request):
    context = {
        'active': 'new_recipe',
        'page_title': 'Создание рецепта',
        'button_label': 'Создать рецепт',
    }
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    if not form.is_valid():
        context['form'] = form
        return render(request, 'recipe_form.html', context)
    recipe = form.save(commit=False)
    recipe.author = request.user
    form.save()
    ingedient_names = request.POST.getlist('nameIngredient')
    ingredient_units = request.POST.getlist('unitsIngredient')
    amounts = request.POST.getlist('valueIngredient')
    products = [get_object_or_404(
        Product.objects.all,
        title=ingedient_names[i],
        unit=ingredient_units[i]
    ) for i in range(len(ingedient_names))]
    ingredients = []
    for i in zip(recipe, products, amounts):
        ingredients.append(Ingredient(
            recipe=recipe, ingredient=products[i], amount=amounts[i]))
    Ingredient.objects.bulk_create(ingredients)
    return redirect('index')


@login_required(login_url='auth/login/')
@require_GET
def get_ingredients(request):
    query = unquote(request.GET.get('query'))
    data = list(Product.objects.filter(
        title__startswith=query
    ).values(
        'title', 'unit'))
    return JsonResponse(data, safe=False)


@login_required(login_url='auth/login/')
def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    context = {
        'recipe_id': recipe_id,
        'page_title': 'Редактирование рецепта',
        'button_label': 'Сохранить',
    }
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    if not form.is_valid():
        context['form'] = form
        return render(request, 'recipe_form.html', context)
    recipe = form.save(commit=False)
    recipe.author = request.user
    form.save()
    new_titles = request.POST.getlist('nameIngredient')
    new_units = request.POST.getlist('unitsIngredient')
    amounts = request.POST.getlist('valueIngredient')
    Ingredient.objects.filter(recipe__id=recipe_id).delete()
    product = [get_object_or_404(
        Product.objects.all,
        title=new_titles[i],
        unit=new_units[i]
    ) for i in range(len(new_titles))]
    new_ingredients = []
    for i in zip(recipe, product, amounts):
        new_ingredients.append(Ingredient(
            recipe=recipe, ingredient=product[i], amount=amounts[i]))
    Ingredient.objects.bulk_create(new_ingredients)
    return redirect('index')


@login_required(login_url='auth/login/')
@require_GET
def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user.is_superuser or request.user == recipe.author:
        recipe.delete()
    return redirect('index')


def page_not_found(request, exception):
    context = {'path': request.path}
    return render(request, 'misc/404.html', context, status=404)
