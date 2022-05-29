"""
    Collect all models for movie
"""

from datetime import date
from django.db import models

from django.contrib.auth.models import User


class Category(models.Model):
    """
    Model for film category
    """

    name = models.CharField('Category', max_length=150)
    description = models.TextField('Description')
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Actor(models.Model):
    """
    Model for actors
    """
    name = models.CharField('Name', max_length=100)
    age = models.PositiveSmallIntegerField('Age', default=0)
    description = models.TextField('Description')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Actor'
        verbose_name_plural = 'Actors'


class Director(models.Model):
    """
    Model for directors
    """
    name = models.CharField('Name', max_length=100)
    age = models.PositiveSmallIntegerField('Age', default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Director'
        verbose_name_plural = 'Directors'


class Genre(models.Model):
    """
    Model for genre
    """
    name = models.CharField('Genre', max_length=100)
    description = models.TextField('Description')
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'


class Movie(models.Model):
    """
    Model for movies
    """
    title = models.CharField('Name', max_length=100)
    description = models.TextField('Description')
    year = models.PositiveSmallIntegerField('Release Year', default=2019)
    country = models.CharField('Country', max_length=30)
    directors = models.ManyToManyField(Director, verbose_name='Directors',
                                       related_name='film_director')
    actors = models.ManyToManyField(Actor, verbose_name='Actors',
                                    related_name='film_actor')
    genres = models.ManyToManyField(Genre, verbose_name='Genres')
    world_premier = models.DateField('Word premier', default=date.today)
    budget = models.PositiveIntegerField('Budget', default=0,
                                         help_text='Set amount in USD')
    fees_is_usa = models.PositiveIntegerField('Fees in USA', default=0,
                                              help_text='Set amount in USD')
    fees_in_world = models.PositiveIntegerField('Fees in World', default=0,
                                                help_text='Set amount in USD')
    category = models.ForeignKey(Category, verbose_name='Category',
                                 on_delete=models.SET_NULL, null=True)
    url = models.SlugField(max_length=130, unique=True)

    def __str__(self):
        return self.title

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)

    class Meta:
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'


class RatingStar(models.Model):
    """
    Model for rating
    """
    value = models.SmallIntegerField('Value', default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = 'Rate star'
        verbose_name_plural = 'Rates star'
        ordering = ['value']


class Rating(models.Model):
    """
    Model for setting rating to certain film
    """
    ip = models.CharField('Ip address', max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE,
                             verbose_name='Star')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE,
                              verbose_name='Movie',
                              related_name='ratings'
                              )

    def __str__(self):
        return f'{self.star} - {self.movie}'

    class Meta:
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'


class Review(models.Model):
    """
    Model for users review
    """
    email = models.EmailField()
    name = models.CharField('Name', max_length=100)
    text = models.TextField('Message', max_length=5000)
    parent = models.ForeignKey('self', verbose_name='Parent',
                               on_delete=models.SET_NULL,
                               related_name='children',
                               blank=True, null=True)
    movie = models.ForeignKey(Movie, verbose_name='movie',
                              on_delete=models.CASCADE,
                              related_name='reviews')

    def __str__(self):
        return f'{self.name} - {self.movie}'

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'


class UserWishes(models.Model):
    """
    Model for user wishes
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    added = models.DateField('Added', default=date.today)

    def __str__(self):
        return f'{self.user.username}: {self.movie.title}: date: {self.added}'


class MovieImdb(models.Model):
    """
    Model for saving films from imdb ip
    """
    unique_id = models.PositiveIntegerField('Unique ID')
    title = models.CharField('Title', max_length=100)
    overview = models.TextField('Overview', default='')
    release_date = models.DateField('Release date', default=date.today)
    vote_count = models.PositiveIntegerField('Vote count', default=0)
    vote_average = models.DecimalField('Vote Average', max_digits=4,
                                       decimal_places=2, default=0)
    media_type = models.CharField('Media Type', max_length=100)

    def __str__(self):
        return f'{self.title}: {self.vote_average}: {self.media_type}'
