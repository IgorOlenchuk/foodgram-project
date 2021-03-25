from django.contrib import admin
from django.conf import settings
from django.conf.urls import handler400, handler404, handler500
from django.contrib.flatpages import views
from django.urls import include, path

handler400 = 'foodgram.views.page_bad_request'
handler404 = 'foodgram.views.page_not_found'
handler500 = 'foodgram.views.server_error'

urlpatterns = [
    path('auth/', include('django.contrib.auth.urls')),
    path('auth/', include('users.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('api/', include('api.urls')),
    path('', include('recipes.urls')),
]

urlpatterns += [
    path('about/', include('django.contrib.flatpages.urls')),
    path('author/', views.flatpage, {'url': '/author/'}, name='author'),
    path(
        'technologis/',
        views.flatpage,
        {'url': '/technologis/'},
        name='technologis'
    ),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += (path("__debug__/", include(debug_toolbar.urls)),)
