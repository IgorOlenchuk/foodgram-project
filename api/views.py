from django.shortcuts import get_object_or_404
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets, mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Category, Genre, Title, Review, Comments
from users.models import User
from .filters import TitleFilter
from .permissions import IsAdminOrReadOnly, IsAuthorAdminModeratorOrReadOnly
from .serializers import (
    CategorySerializer, GenreSerializer, TitleReadSerializer,
    TitleWriteSerializer, CommentsSerializer, ReviewSerializer
)


class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(rating=Avg('review__score'))
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAuthorAdminModeratorOrReadOnly,
    ]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        reviews = title.review.all()
        return reviews

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        serializer.save(author=self.request.user, title=title)


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAuthorAdminModeratorOrReadOnly,
    ]

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get("review_id"),
            title__id=self.kwargs.get("title_id")
        )
        return review.comments.all()

    def perform_create(self, serializer, **kwargs):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get("review_id"),
            title__id=self.kwargs.get("title_id")
        )
        serializer.save(author=self.request.user, review=review)
