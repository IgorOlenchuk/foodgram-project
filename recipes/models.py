from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название продукта')
    unit = models.CharField(max_length=255, verbose_name='Единицы измерения')

    class Meta:
        verbose_name_plural = 'Ингредиенты'
        verbose_name = 'Ингредиенты'

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
        Product, through='Ingredient', related_name='recipeIngredients')
    cook_time = models.PositiveIntegerField(verbose_name='Время приготовления')
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Время публикации', db_index=True)
    favorite_by = models.ManyToManyField(User, through='Favorite',
                                         related_name='favorite_recipes',
                                         blank=True)
    purchase_by = models.ManyToManyField(User, through='Purchase',
                                         related_name='shop_list',
                                         blank=True)

    class Meta:
        ordering = ['-pub_date']
        verbose_name_plural = 'Рецепты'
        verbose_name = 'Рецепты'

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


class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    created = models.DateTimeField('date of creation', auto_now_add=True)

    class Meta:
        ordering = ['-created']
        verbose_name_plural = 'Список покупок'
        verbose_name = 'Список покупок'

    def __str__(self):
        return f'{self.recipe}'


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    created = models.DateTimeField('date published', auto_now_add=True)

    class Meta:
        ordering = ['-created']
        verbose_name_plural = 'Избранное'
        verbose_name = 'Избранное'

    def __str__(self):
        return f'{self.recipe}'
