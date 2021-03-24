from rest_framework import filters, viewsets, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Favorite, Subscription
from .permissions import IsAuthorOrAdmin
from .serializers import (
    FavoriteSerializer, IngredientSerializer, PurchaseSerializer,
    SubscriptionSerializer
)
from recipes.models import Ingredient


class IngredientViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^title',)


class CreateDestroyViewSet(mixins.CreateModelMixin,
                           mixins.DestroyModelMixin,
                           viewsets.GenericViewSet):
    pass


class SubscriptionViewSet(CreateDestroyViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated, IsAuthorOrAdmin)
    lookup_field = 'author'


class FavoriteViewSet(CreateDestroyViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = (AllowAny,)
    lookup_field = 'recipe'


class PurchaseViewSet(mixins.ListModelMixin, CreateDestroyViewSet):
    serializer_class = PurchaseSerializer
    permission_classes = (IsAuthenticated, IsAuthorOrAdmin)
    lookup_field = 'recipe'

    def get_queryset(self):
        return self.request.user.purchases.all()
