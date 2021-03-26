from django.contrib.auth import get_user_model
from django.db import models

from .managers import RecipeManager

User = get_user_model()


class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название продукта')
    unit = models.CharField(max_length=255, verbose_name='Единицы измерения')

    def __str__(self):
        return f'{self.title}, {self.unit}'


class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название тега')
    slug = models.SlugField(verbose_name='Слаг тега')

    def __str__(self):
        return f'{self.name}'


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name='Автор рецепта',
                               related_name='recipes')
    name = models.CharField(max_length=255, verbose_name='Название рецепта')
    description = models.TextField(verbose_name='Описание рецепта')
    image = models.ImageField(upload_to='recipes/',
                              verbose_name='Изображение блюда')
    tags = models.ManyToManyField(Tag, verbose_name='Теги', blank=True)
    ingredients = models.ManyToManyField(
        Product, through='Ingredient', related_name='RecipeIngredients')
    cook_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Время публикации', db_index=True)

    recipes = RecipeManager()

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return f'{self.name}'


class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.FloatField(verbose_name='Количество ингредиента')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'amount', 'recipe'],
                name='unique_ingredient'
            )
        ]

    def __str__(self):
        return f'{self.amount}'


class PurchaseManager(models.Manager):
    def counter(self, user):
        try:
            return super().get_queryset().get(user=user).recipes.count()
        except User.DoesNotExist:
            return 0

    def get_purchases_list(self, user):
        try:
            return super().get_queryset().get(user=user).recipes.all()
        except User.DoesNotExist:
            return []

    def get_user_purchase(self, user):
        try:
            return super().get_queryset().get(user=user)
        except User.DoesNotExist:
            purchase = Purchase(user=user)
            purchase.save()
            return purchase


class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipes = models.ManyToManyField(Recipe)

    purchase = PurchaseManager()

    class Meta:
        verbose_name = 'покупка'
        verbose_name_plural = 'покупки'


class FavoriteManager(models.Manager):
    def get_favorites(self, user):
        try:
            return super().get_queryset().get(user=user).recipes.all()
        except User.DoesNotExist:
            return []

    def get_tag_filtered(self, user, tags):
        try:
            recipes = super().get_queryset().get(user=user).recipes.all()
            if tags:
                return recipes.prefetch_related(
                    'author', 'tags'
                ).filter(
                    tags__slug__in=tags
                ).distinct()
            else:
                return recipes.prefetch_related(
                    'author', 'tags'
                ).all()
        except User.DoesNotExist:
            return []

    def get_user(self, user):
        try:
            return super().get_queryset().get(user=user)
        except User.DoesNotExist:
            favorite_user = Favorite(user=user)
            favorite_user.save()
            return favorite_user


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipes = models.ManyToManyField(Recipe)

    favorite = FavoriteManager()

    class Meta:
        verbose_name = 'избранный'
        verbose_name_plural = 'избранные'