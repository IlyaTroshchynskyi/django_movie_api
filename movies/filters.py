"""
    Collect filters for movie app
"""

from django_filters import rest_framework as filters

from .models import Movie, Actor


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class MovieFilter(filters.FilterSet):
    """
    Filters for movie
    """
    genres = CharFilterInFilter(field_name='genres__name', lookup_expr='in')
    actors = CharFilterInFilter(field_name='actors__name', lookup_expr='in')
    directors = CharFilterInFilter(field_name='directors__name', lookup_expr='in')
    title = CharFilterInFilter(field_name='title', lookup_expr='in')
    year = filters.RangeFilter()

    class Meta:
        model = Movie
        fields = ['genres', 'year', 'directors', 'actors', 'title']


class ActorBasedMovie(filters.FilterSet):
    """
    Find the actors who played in the film with the name X
    """

    title = CharFilterInFilter(field_name='film_actor__title', lookup_expr='in')

    class Meta:
        model = Actor
        fields = ['title', ]
