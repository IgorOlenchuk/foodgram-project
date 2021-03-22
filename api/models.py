from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.PositiveIntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    genre = models.ManyToManyField(Genre, blank=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="review")
    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              related_name="review")
    text = models.TextField()
    score = models.PositiveIntegerField(validators=[MinValueValidator(1),
                                       MaxValueValidator(10)], null=True)
    pub_date = models.DateTimeField("Дата добавления", auto_now_add=True,
                                    db_index=True)

    def __str__(self):
        return self.text


class Comments(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="comments")
    review = models.ForeignKey(Review, on_delete=models.CASCADE,
                               related_name="comments")
    text = models.TextField()
    pub_date = models.DateTimeField("Дата добавления", auto_now_add=True,
                                   db_index=True)

    class Meta:
        ordering = ("-pub_date",)
        
    def __str__(self):
        return self.text
