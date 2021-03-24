from django.urls import include, path

from . import views

recipe_urls = [
    path("new/", views.new_recipe, name="new_recipe"),
    path(
        '<int:recipe_id>/<slug:slug>/',
        views.recipe_view_slug, name='recipe_view_slug'
    ),
    path(
        '<int:recipe_id>/', views.recipe_view,
        name='recipe_view'
    ),
    path(
        '<int:recipe_id>/<slug:slug>/edit/',
        views.recipe_edit, name='edit_recipe'
    ),
    path(
        '<int:recipe_id>/<slug:slug>/delete/',
        views.recipe_delete, name='recipe_delete'
    ),
]

purchases_urls = [
    path('', views.purchases, name='purchases'),
    path('download/', views.purchases_download, name='purchases_download'),
]

urlpatterns = [
    path("", views.index, name="index"),
    path('subscriptions/', views.subscriptions, name='subscriptions'),
    path('favorites/', views.favorites, name='favorites'),
    path('<str:username>/', views.profile, name='profile_view'),
    path('purchases/', include(purchases_urls)),
    path('recipes/', include(recipe_urls)),
]
