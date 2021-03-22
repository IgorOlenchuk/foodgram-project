from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet,
                    GenreViewSet,
                    TitleViewSet,
                    ReviewViewSet,
                    CommentsViewSet)
from users.views import (UserViewSet,
                        CodeGenerationViewSet,
                        TokenGenerationViewSet)

router_v1 = DefaultRouter()


router_v1.register(r'users', UserViewSet, basename='user')
router_v1.register(r'auth/email', CodeGenerationViewSet, basename='send_code')
router_v1.register(r'auth/token', TokenGenerationViewSet, basename='send_token')
router_v1.register(r'categories', CategoryViewSet, basename='categories')
router_v1.register(r'genres', GenreViewSet, basename='genres')
router_v1.register(r'titles', TitleViewSet, basename='titles')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
