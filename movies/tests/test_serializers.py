from django.contrib.auth.models import User
from django.db import models
from django.test import TestCase
from django.urls import reverse
from django.test.client import RequestFactory

from movies.models import Category, Rating, RatingStar, Movie, Actor, Genre, \
    UserWishes, Review, Director
from movies.serializers import CategorySerializer, \
    CreateRatingSerializer, ActorSerializer, GenreSerializer, \
    MovieListSerializer, MovieDetailSerializer, \
    WishesCreateSerializer, WishesSerializer, RatingSerializer, \
    UserSerializer, ReviewCreateSerializer, DirectorSerializer


from movies.utils import get_client_ip


class SerializersTestCase(TestCase):

    def setUp(self):
        self.category_1 = Category.objects\
            .create(name='Film', description='First Cat', url='film')
        self.category_2 = Category.objects\
            .create(name='Serial', description='Second Cat', url='serial')

        self.actor_1 = Actor.objects\
            .create(name='Джейсон Стетхем', age=40, description='Описание')
        self.actor_2 = Actor.objects\
            .create(name='Джейсон Стетхем2', age=42, description='Описание')

        self.director_1 = Director.objects.create(name='Director1', age=40)
        self.director_2 = Director.objects.create(name='Director2', age=42)

        self.genre_1 = Genre.objects\
            .create(name='Adventure', description='Adventure', url='adventure')
        self.genre_2 = Genre.objects\
            .create(name='Horror', description='Horror', url='horror')

        self.star_1 = RatingStar.objects.create(value=1)
        self.star_2 = RatingStar.objects.create(value=2)

        self.movie_1 = Movie.objects.create(title='Test',
                                            description='Test',
                                            world_premier='2022-04-28',
                                            year=2019, country='USA', budget=100,
                                            fees_is_usa=150, fees_in_world=200,
                                            category=Category.objects.all()[0],
                                            url='test')

        self.movie_2 = Movie.objects.create(title='ForsazhS',
                                            description='ForsazhS',
                                            world_premier='2022-04-28',
                                            year=2019, country='USA', budget=100,
                                            fees_is_usa=150, fees_in_world=200,
                                            category=Category.objects.all()[0],
                                            url='forsazhs')
        self.movie_1.directors.add(self.director_1)
        self.movie_1.actors.add(self.actor_1)
        self.movie_1.genres.add(self.genre_1)

        self.user_1 = User.objects.create_user('test', 'test@mail.ua', '12345')
        self.wishes_1 = UserWishes.objects\
            .create(user=self.user_1, movie=self.movie_1)
        self.wishes_2 = UserWishes.objects\
            .create(user=self.user_1, movie=self.movie_2)

        self.rating_1 = Rating.objects\
            .create(ip='1.1.1.1', star=self.star_1, movie=self.movie_1)
        self.rating_2 = Rating.objects\
            .create(ip='2.1.1.1', star=self.star_2, movie=self.movie_2)

        self.review_1 = Review.objects.create(email='test1@mail.ru', name='Carl',
                                              text='Good film',
                                              movie=self.movie_1)
        self.review_2 = Review.objects.create(email='test1@mail.ru', name='Carl',
                                              text='Good film Children',
                                              parent=self.review_1,
                                              movie=self.movie_1)
        self.review_3 = Review.objects.create(email='test2@mail.ru', name='Carl1',
                                              text='Good film',
                                              movie=self.movie_1)

    def test_category_serializer(self):
        result = CategorySerializer([self.category_1, self.category_2],
                                    many=True).data
        expected_data = [
            {
                'id': self.category_1.id,
                'name': 'Film',
                'description': 'First Cat',
                'url': 'film'
            },
            {
                'id': self.category_2.id,
                'name': 'Serial',
                'description': 'Second Cat',
                'url': 'serial'
            }]
        self.assertEqual(expected_data, result)

    def test_actor_serializer(self):
        result = ActorSerializer([self.actor_1, self.actor_2], many=True).data
        expected_data = [
            {
                'id': self.actor_1.id,
                'name': 'Джейсон Стетхем',
                'age': 40,
                'description': 'Описание'
            },
            {
                'id': self.actor_2.id,
                'name': 'Джейсон Стетхем2',
                'age': 42,
                'description': 'Описание'
            }]
        self.assertEqual(expected_data, result)

    def test_director_serializer(self):
        result = DirectorSerializer([self.director_1, self.director_2],
                                    many=True).data
        expected_data = [
            {
                'id': self.director_1.id,
                'name': 'Director1',
                'age': 40
            },
            {
                'id': self.director_2.id,
                'name': 'Director2',
                'age': 42,
            }]
        self.assertEqual(expected_data, result)

    def test_genre_serializer(self):
        result = GenreSerializer([self.genre_1, self.genre_2], many=True).data

        expected_data = [
            {
                'id': self.genre_1.id,
                'name': 'Adventure',
                'description': 'Adventure',
                'url': 'adventure'
            },
            {
                'id': self.genre_2.id,
                'name': 'Horror',
                'description': 'Horror',
                'url': 'horror'
            }]
        self.assertEqual(expected_data, result)

    def test_movie_list_serializer(self):
        url = reverse('movie-list')
        factory = RequestFactory()
        request = factory.get(url)
        movies = Movie.objects.all().annotate(
            rating_user=models.Count("ratings", filter=models
                                     .Q(ratings__ip=get_client_ip(request)))
        ).annotate(
            middle_star=models
                            .Sum(models.F('ratings__star__value')) / models
                .Count(models.F('ratings'))
        ).order_by('id')
        result = MovieListSerializer(movies, many=True).data

        expected_data = [
            {
                'id': self.movie_1.id,
                'title': 'Test',
                'description': 'Test',
                'year': 2019,
                'country': 'USA',
                'directors': [self.director_1.id],
                'actors': [self.actor_1.id],
                'genres': [self.genre_1.id],
                'world_premier': '2022-04-28',
                'budget': 100,
                'fees_is_usa': 150,
                'fees_in_world': 200,
                'category': self.category_1.id,
                'rating_user': False,
                'middle_star': 1,
                'url': 'test'
            },
            {
                'id': self.movie_2.id,
                'title': 'ForsazhS',
                'description': 'ForsazhS',
                'year': 2019,
                'country': 'USA',
                'directors': [],
                'actors': [],
                'genres': [],
                'world_premier': '2022-04-28',
                'budget': 100,
                'fees_is_usa': 150,
                'fees_in_world': 200,
                'category': self.category_1.id,
                'rating_user': False,
                'middle_star': 2,
                'url': 'forsazhs'
            }
        ]

        self.assertEqual(expected_data, result)

    def test_movie_detail_serializer(self):
        movie = Movie.objects.get(id=self.movie_1.id)
        result = MovieDetailSerializer(movie).data

        expected_data = {
            'id': self.movie_1.id,
            'category':
                {
                    'id': self.category_1.id,
                    'name': 'Film',
                    'description': 'First Cat',
                    'url': 'film'
                },
            'directors': [
                {
                    'id': self.director_1.id,
                    'name': 'Director1',
                    'age': 40
                }],
            'actors': [
                {
                    'id': self.actor_1.id,
                    'name': 'Джейсон Стетхем',
                    'age': 40,
                    'description': 'Описание'
                }],
            'genres': [
                {
                    'id': self.genre_1.id,
                    'name': 'Adventure',
                    'description': 'Adventure',
                    'url': 'adventure'
                }],
            'reviews':
                [
                    {'id': self.review_1.id, 'name': 'Carl',
                     'text': 'Good film', 'children':
                        [{'id': self.review_2.id, 'name': 'Carl',
                          'text': 'Good film Children',
                          'children': []}]
                     },
                    {'id': self.review_3.id, 'name': 'Carl1',
                     'text': 'Good film', 'children': []}],
            'title': 'Test', 'description': 'Test', 'year': 2019,
            'country': 'USA',
            'world_premier': '2022-04-28', 'budget': 100, 'fees_is_usa': 150,
            'fees_in_world': 200, 'url': 'test'

        }
        self.assertEqual(expected_data, result)

    def test_post_user_wishes_serializer(self):
        result = WishesCreateSerializer(self.wishes_1).data
        expected_data = {
            "movie": self.wishes_1.id
        }
        self.assertEqual(expected_data, result)

    def test_list_wishes_serializer(self):
        result = WishesSerializer([self.wishes_1], many=True).data
        expected_data = [
            {
                "id": self.wishes_1.id,
                "movie": {
                    'id': self.movie_1.id,
                    'title': 'Test',
                    'description': 'Test',
                    'year': 2019,
                    'country': 'USA',
                    'directors': [self.director_1.id],
                    'actors': [self.actor_1.id],
                    'genres': [self.genre_1.id],
                    'world_premier': '2022-04-28',
                    'budget': 100,
                    'fees_is_usa': 150,
                    'fees_in_world': 200,
                    'category': self.category_1.id,
                    'url': 'test'
                },
                "user": {
                    "id": self.user_1.id,
                    "username": "test",
                    "email": "test@mail.ua"
                },
                "added": self.wishes_1.added.strftime("%Y-%m-%d")
            }
        ]

        self.assertEqual(expected_data, result)

    def test_rating_serializer(self):
        result = RatingSerializer([self.star_1, self.star_2], many=True).data
        expected_data = [
            {
                'id': self.star_1.id,
                'value': 1,
            },
            {
                'id': self.star_2.id,
                'value': 2
            }]
        self.assertEqual(expected_data, result)

    def test_user_serializer(self):
        result = UserSerializer(self.user_1).data
        expected_data = {
            'id': self.user_1.id,
            'username': 'test',
            'email': 'test@mail.ua'
        }

        self.assertEqual(expected_data, result)

    def test_create_rating_serializer(self):
        result = CreateRatingSerializer(self.rating_1).data
        expected_data = {
            'star': self.star_1.id,
            'movie': self.movie_1.id,
        }
        self.assertEqual(expected_data, result)

    def test_create_review_serializer(self):
        result = ReviewCreateSerializer(self.review_2).data
        expected_data = {
            "id": self.review_2.id,
            "email": "test1@mail.ru",
            "name": "Carl",
            "text": "Good film Children",
            "movie": self.movie_1.id,
            "parent": self.review_1.id
        }
        self.assertEqual(expected_data, result)
