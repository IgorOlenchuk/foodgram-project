from django.contrib import admin

from users.models import User
from .models import Category, Genre, Title, Review, Comments


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'

admin.site.register(Category, CategoryAdmin)


class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'

admin.site.register(Genre, GenreAdmin)


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'category', 'genres',)
    search_fields = ('name',)
    list_filter = ('year',)
    empty_value_display = '-пусто-'

    def genres(self, obj):
        return "\n".join([genre.slug for genre in obj.genre.all()])

admin.site.register(Title, TitleAdmin)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'title', 'text', 'score', 'pub_date',)
    search_fields = ('title',)
    empty_value_display = '-пусто-'

admin.site.register(Review, ReviewAdmin)


class CommentsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'review', 'text', 'pub_date',)
    search_fields = ('review',)
    empty_value_display = '-пусто-'

admin.site.register(Comments, CommentsAdmin)