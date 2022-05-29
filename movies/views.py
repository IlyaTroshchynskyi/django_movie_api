"""
Collect all api call for app movies
"""


from django.db import models

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_view, extend_schema, \
    OpenApiParameter
from rest_framework import generics, viewsets

from rest_framework.permissions import IsAuthenticatedOrReadOnly


from .models import Movie, Category, Actor, Genre, UserWishes, RatingStar, \
    Director
from .serializers import MovieListSerializer, MovieDetailSerializer, \
    CategorySerializer, ReviewCreateSerializer, CreateRatingSerializer, \
    ActorSerializer, GenreSerializer, WishesSerializer, \
    WishesCreateSerializer, RatingSerializer, DirectorSerializer

from .utils import get_client_ip
from .filters import MovieFilter, ActorBasedMovie


class CategoryView(viewsets.ModelViewSet):
    """
    View for get, create, update, delete category
    """

    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]


@extend_schema_view(
    list=extend_schema(parameters=[
        OpenApiParameter("title", OpenApiTypes.STR, OpenApiParameter.QUERY,
                         description='Set the titles of movies'),
    ], description='Filter actors by movie'))
class ActorViews(viewsets.ModelViewSet):
    """
    View for get, create, update, delete actors
    """
    serializer_class = ActorSerializer
    queryset = Actor.objects.all()
    filterset_class = ActorBasedMovie
    permission_classes = [IsAuthenticatedOrReadOnly]


class DirectorViews(viewsets.ModelViewSet):
    """
    View for get, create, update, delete directors
    """
    serializer_class = DirectorSerializer
    queryset = Director.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]


class GenresViews(viewsets.ModelViewSet):
    """
    View for get, create, update, delete actors
    """

    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]


@extend_schema_view(
    list=extend_schema(parameters=[
        OpenApiParameter("genres", OpenApiTypes.STR, OpenApiParameter.QUERY,
                         description='Set the genres'),
        OpenApiParameter("actors", OpenApiTypes.STR, OpenApiParameter.QUERY,
                         description='Set actors for filter'),
        OpenApiParameter("directors", OpenApiTypes.STR, OpenApiParameter.QUERY,
                         description='Set directors for filter'),
        OpenApiParameter("title", OpenApiTypes.STR, OpenApiParameter.QUERY,
                         description='Set film title for filter'),
        OpenApiParameter("year_min", OpenApiTypes.NUMBER, OpenApiParameter.QUERY,
                         description='Set year start'),
        OpenApiParameter("year_max", OpenApiTypes.NUMBER, OpenApiParameter.QUERY,
                         description='Set year end')
    ], description='View to get movie with full list or use query params'))
class MovieViews(viewsets.ModelViewSet):
    """
    View for get, create, update, delete movie
    """
    filterset_class = MovieFilter
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        Returns the queryset that should be used for list views,
        and that should be used as the base for lookups in detail views.
        """

        if self.action == 'list':

            movies = (
                Movie.objects.all()
                    .prefetch_related('directors', 'actors', 'genres')
                    .annotate(
                    rating_user=models
                        .Count("ratings",
                               filter=models.Q(ratings__ip=get_client_ip(
                                   self.request)))
                ).annotate(
                    middle_star=models
                                    .Sum(models.F('ratings__star__value')
                                         ) / models.Count(models.F('ratings'))
                )
            )
            return movies
        return (Movie.objects.all()
                .prefetch_related('reviews', 'directors', 'actors', 'genres')
                )

    def get_serializer_class(self):
        """
        Returns the class that should be used for the serializer.
        """
        if self.action == 'list':
            return MovieListSerializer
        if self.action == "retrieve":
            return MovieDetailSerializer
        return MovieListSerializer


class ReviewCreateView(generics.CreateAPIView):
    """
    View creating review for films
    """
    serializer_class = ReviewCreateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class AddStarRatingView(generics.CreateAPIView):
    """
    View for setting rating for films
    """

    serializer_class = CreateRatingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        """
        Override of the method from mixin. Set new property ip from request object
        :param serializer:
        :return: None
        """
        serializer.save(ip=get_client_ip(self.request))


class WishesCreateView(viewsets.mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    View for creating user wishes
    """

    serializer_class = WishesCreateSerializer
    queryset = UserWishes.objects.all()

    permission_classes = [IsAuthenticatedOrReadOnly, ]

    def perform_create(self, serializer):
        """
        Override of the method from mixin.
        Set new property user from request object for setting auth user property
        :param serializer:
        :return: None
        """
        serializer.save(user=self.request.user)


class WishesRetrieveDeleteView(viewsets.mixins.ListModelMixin,
                               viewsets.mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):

    """
    View for deleting and retrieving user wishes
    """
    serializer_class = WishesSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        Returns the queryset that should be used for list views,
        and that should be used as the base for lookups in detail views.
        """
        users_wishes = (
            UserWishes.objects.select_related('movie')
                .prefetch_related('movie__directors',
                                  'movie__actors', 'movie__genres')
            .filter(user=self.request.user.id))
        return users_wishes


class RatingView(viewsets.mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    View for getting list available ratings
    """
    serializer_class = RatingSerializer
    queryset = RatingStar.objects.all()
