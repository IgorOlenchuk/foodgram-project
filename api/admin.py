from django.contrib import admin

from .models import Favorite, Purchase, Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author')
    autocomplete_fields = ('user', 'author')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipes')
    autocomplete_fields = ('user', 'recipes')


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipes')
    autocomplete_fields = ('user', 'recipes')
