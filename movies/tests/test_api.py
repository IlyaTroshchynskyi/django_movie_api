import json

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.test.client import RequestFactory

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from movies.models import Category, Rating, RatingStar, Movie, Actor, Genre, \
    UserWishes, Review, Director
from movies.serializers import CategorySerializer, ActorSerializer, \
    GenreSerializer, MovieListSerializer, MovieDetailSerializer, \
    WishesSerializer, RatingSerializer, DirectorSerializer

from movies.utils import get_client_ip


class MovieApiTestCase(APITestCase):

    def setUp(self):

        self.category_1 = Category.objects\
            .create(name='Film', description='First Cat', url='film')
        self.category_2 = Category.objects\
            .create(name='Serial', description='Second Cat', url='serial')

        self.actor_1 = Actor.objects.create(name='Джейсо Стетхем', age=40,
                                            description='Описание')
        self.actor_2 = Actor.objects.create(name='Джейсо Стетхем2', age=42,
                                            description='Описание')

        self.director_1 = Director.objects.create(name='Director1', age=40)
        self.director_2 = Director.objects.create(name='Director2', age=42)

        self.genre_1 = Genre.objects\
            .create(name='Adventure', description='Adventure', url='adventure')
        self.genre_2 = Genre.objects.create(name='Horror', description='Horror',
                                            url='horror')

        self.star_1 = RatingStar.objects.create(value=1)
        self.star_2 = RatingStar.objects.create(value=2)

        self.movie_1 = Movie.objects\
            .create(title='Forsazh1', description='Forsazh1', year=2019,
                    country='USA', budget=100, fees_is_usa=150, fees_in_world=200,
                    world_premier='2022-04-28',
                    category=Category.objects.all()[0],
                    url='forsazh1')

        self.movie_2 = Movie.objects\
            .create(title='Forsazh2', description='Forsazh2', year=2019,
                    country='USA',
                    budget=100, fees_is_usa=150, fees_in_world=200,
                    world_premier='2022-04-28',
                    category=Category.objects.all()[0],
                    url='forsazh2')

        self.movie_1.directors.add(self.director_1)
        self.movie_1.actors.add(self.actor_1)
        self.movie_1.genres.add(self.genre_1)

        self.user_1 = User.objects.create_user('test', 'test@mail.ua', '12345')
        self.wishes_1 = UserWishes.objects.create(user=self.user_1,
                                                  movie=self.movie_1)
        self.wishes_2 = UserWishes.objects.create(user=self.user_1,
                                                  movie=self.movie_2)

        self.rating_1 = Rating.objects.create(ip='1.1.1.1', star=self.star_1,
                                              movie=self.movie_1)
        self.rating_2 = Rating.objects.create(ip='2.1.1.1', star=self.star_2,
                                              movie=self.movie_2)

        self.review_1 = Review.objects.create(email='test1@mail.ru', name='Carl',
                                              text='Good film',
                                              movie=self.movie_1)
        self.review_2 = Review.objects.create(email='test1@mail.ru', name='Carl',
                                              text='Good film',
                                              parent=self.review_1,
                                              movie=self.movie_1)
        self.review_3 = Review.objects.create(email='test2@mail.ru', name='Carl1',
                                              text='Good film',
                                              movie=self.movie_1)

    def test_get_category(self):
        response = self.client.get('/api/v1/category/')
        test_data = CategorySerializer([self.category_1, self.category_2],
                                       many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(test_data, response.data.get('results'))

    def test_get_category_detail(self):
        url = reverse('category-detail', args=(self.category_1.id, ))
        response = self.client.get(url)
        test_data = CategorySerializer(self.category_1).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(test_data, response.data)

    def test_post_category(self):
        url = reverse('category-list')
        self.assertEqual(2, Category.objects.all().count())
        data = {
            "name": "Movie",
            "description": "Movie",
            "url": "movie"
        }
        json_data = json.dumps(data)
        refresh = RefreshToken.for_user(self.user_1)

        self.client_class\
            .credentials(self.client,
                         HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        response = self.client.post(url, data=json_data,
                                    content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(3, Category.objects.all().count())

    def test_put_category(self):
        data = {
            "name": "Film_updated",
            "description": self.category_1.description,
            "url": self.category_1.url
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user_1)
        response = self.client\
            .put('/api/v1/category/' + str(self.category_1.id) + '/',
                 data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.category_1.refresh_from_db()
        self.assertEqual("Film_updated", self.category_1.name)

    def test_delete_category(self):
        self.client.force_login(self.user_1)
        response = self.client\
            .delete('/api/v1/category/' + str(self.category_1.id) + '/')

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_get_actors(self):
        url = reverse('actor-list')
        response = self.client.get(url)
        test_data = ActorSerializer([self.actor_1, self.actor_2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(test_data, response.data.get('results'))

    def test_get_actor_detail(self):
        url = reverse('actor-detail', args=(self.actor_1.id, ))
        response = self.client.get(url)
        test_data = ActorSerializer(self.actor_1).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(test_data, response.data)

    def test_get_actors_by_movie_name(self):
        response = self.client.get('/api/v1/actor/?title=' + self.movie_1.title)
        test_data = ActorSerializer([self.actor_1], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(test_data[0], response.data.get('results')[0])
        self.assertEqual(len(response.data.get('results')), 1)

    def test_post_actor(self):
        url = reverse('actor-list')
        self.assertEqual(2, Actor.objects.all().count())
        data = {
            "name": "Actor_Test",
            "age": 10,
            "description": "Actor_Test_DSC"
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user_1)
        response = self.client.post(url, data=json_data,
                                    content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(3, Actor.objects.all().count())

    def test_put_actor(self):
        url = reverse('actor-detail', args=(self.actor_1.id, ))
        data = {
            "name": "Actor_Test",
            "age": self.actor_1.age,
            "description": self.actor_1.description
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user_1)
        response = self.client.put(url, data=json_data,
                                   content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.actor_1.refresh_from_db()
        self.assertEqual("Actor_Test", self.actor_1.name)

    def test_delete_actor(self):
        self.client.force_login(self.user_1)
        url = reverse('actor-detail', args=(self.actor_1.id,))
        response = self.client.delete(url)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_get_director(self):
        url = reverse('director-list')
        response = self.client.get(url)
        test_data = DirectorSerializer([self.director_1, self.director_2],
                                       many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(test_data, response.data.get('results'))

    def test_get_director_detail(self):
        url = reverse('director-detail', args=(self.director_1.id, ))
        response = self.client.get(url)
        test_data = DirectorSerializer(self.director_1).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(test_data, response.data)

    def test_post_director(self):
        url = reverse('director-list')
        self.assertEqual(2, Director.objects.all().count())
        data = {
            "name": "Director_Test",
            "age": 10
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user_1)
        response = self.client.post(url, data=json_data,
                                    content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(3, Director.objects.all().count())

    def test_put_director(self):
        url = reverse('director-detail', args=(self.director_1.id, ))
        data = {
            "name": "Director_Test",
            "age": self.director_1.age
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user_1)
        response = self.client.put(url, data=json_data,
                                   content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.director_1.refresh_from_db()
        self.assertEqual("Director_Test", self.director_1.name)

    def test_delete_director(self):
        self.client.force_login(self.user_1)
        url = reverse('director-detail', args=(self.director_1.id,))
        response = self.client.delete(url)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_get_genres(self):
        url = reverse('genre-list')
        response = self.client.get(url)
        test_data = GenreSerializer([self.genre_1, self.genre_2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(test_data, response.data.get('results'))

    def test_get_genre_detail(self):
        url = reverse('genre-detail', args=(self.genre_1.id, ))
        response = self.client.get(url)
        test_data = GenreSerializer(self.genre_1).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(test_data, response.data)

    def test_post_genre(self):
        url = reverse('genre-list')
        self.assertEqual(2, Genre.objects.all().count())
        data = {
            "name": "Test",
            "description": "Test",
            "url": "test"
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user_1)
        response = self.client.post(url, data=json_data,
                                    content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(3, Genre.objects.all().count())

    def test_put_genre(self):
        url = reverse('genre-detail', args=(self.genre_1.id, ))
        data = {
            "name": "Updated_Genre",
            "description": self.genre_1.description,
            "url": self.genre_1.url
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user_1)
        response = self.client.put(url, data=json_data,
                                   content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.genre_1.refresh_from_db()
        self.assertEqual("Updated_Genre", self.genre_1.name)

    def test_delete_genre(self):
        self.client.force_login(self.user_1)
        url = reverse('genre-detail', args=(self.genre_1.id,))
        response = self.client.delete(url)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_get_movie(self):
        url = reverse('movie-list')
        response = self.client.get(url)
        factory = RequestFactory()
        request = factory.get(url)
        movies = Movie.objects.all().annotate(
            rating_user=models
                .Count("ratings", filter=models
                       .Q(ratings__ip=get_client_ip(request)))
        ).annotate(
            middle_star=models
                            .Sum(models.F('ratings__star__value')) / models
                .Count(models.F('ratings'))
        ).order_by('id')
        test_data = MovieListSerializer(movies, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(test_data, response.data.get('results'))

    def test_get_movie_detail(self):
        url = reverse('movie-detail', args=(self.movie_1.id, ))
        response = self.client.get(url)
        test_data = MovieDetailSerializer(self.movie_1).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(test_data, response.data)

    def test_movie_filter_by_name(self):
        response = self.client.get('/api/v1/movie/?title=' + self.movie_1.title)
        test_data = MovieListSerializer([self.movie_1], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(test_data[0].get('title'),
                         response.data.get('results')[0].get('title'))
        self.assertEqual(len(response.data.get('results')), 1)

    def test_movie_filter_by_actor_name(self):
        response = self.client.get('/api/v1/movie/?actors=' + self.actor_1.name)
        test_data = MovieListSerializer([self.movie_1], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(test_data[0].get('title'),
                         response.data.get('results')[0].get('title'))
        self.assertEqual(len(response.data.get('results')), 1)
        self.assertEqual(self.actor_1.id,
                         response.data.get('results')[0].get('actors')[0])

    def test_movie_filter_by_genre(self):
        response = self.client.get('/api/v1/movie/?genres=' + self.genre_1.name)
        test_data = MovieListSerializer([self.movie_1], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(test_data[0].get('title'),
                         response.data.get('results')[0].get('title'))
        self.assertEqual(len(response.data.get('results')), 1)
        self.assertEqual(self.genre_1.id,
                         response.data.get('results')[0].get('genres')[0])

    def test_movie_filter_by_directors(self):
        response = self.client\
            .get('/api/v1/movie/?directors=' + self.director_1.name)
        test_data = MovieListSerializer([self.movie_1], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(test_data[0].get('title'),
                         response.data.get('results')[0].get('title'))
        self.assertEqual(len(response.data.get('results')), 1)
        self.assertEqual(self.actor_1.id,
                         response.data.get('results')[0].get('directors')[0])

    def test_post_movie(self):
        url = reverse('movie-list')
        self.assertEqual(2, Movie.objects.all().count())
        data = {
            "title": "Test",
            "description": "test_description",
            "year": 2023,
            "country": "USA",
            "directors": [self.director_1.id],
            "actors": [self.actor_2.id],
            "genres": [self.genre_1.id, self.genre_2.id],
            "budget": 20,
            "fees_is_usa": 25,
            "fees_in_world": 27,
            "category": self.category_1.id,
            "url": "test"
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user_1)
        response = self.client.post(url, data=json_data,
                                    content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(3, Movie.objects.all().count())

    def test_put_movie(self):
        url = reverse('movie-detail', args=(self.movie_1.id, ))
        data = {
            "title": "Forsazh_updated",
            "description": "Forsazh1",
            "year": 2019,
            "country": "USA",
            "directors": [self.director_1.id],
            "actors": [self.actor_1.id],
            "genres": [self.genre_1.id],
            "world_premier": '2022-04-28',
            "budget": 100,
            "fees_is_usa": 150,
            "fees_in_world": 200,
            "category": self.category_1.id,
            "url": "forsazh1"
        }

        json_data = json.dumps(data)
        self.client.force_login(self.user_1)
        response = self.client.put(url, data=json_data,
                                   content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.movie_1.refresh_from_db()
        self.assertEqual("Forsazh_updated", self.movie_1.title)
        self.assertEqual(2, Movie.objects.all().count())

    def test_delete_movie(self):
        self.client.force_login(self.user_1)
        url = reverse('movie-detail', args=(self.movie_1.id,))
        response = self.client.delete(url)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_get_user_wishes(self):
        url = reverse('user_wishes-list')
        self.client.force_login(self.user_1)
        response = self.client.get(url)
        test_data = WishesSerializer([self.wishes_1, self.wishes_2],
                                     many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(test_data, response.data.get('results'))

    def test_post_user_wishes(self):
        url = reverse('create_wishes-list')
        self.assertEqual(2, UserWishes.objects.all().count())
        data = {
            "movie": self.movie_1.id
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user_1)
        response = self.client.post(url, data=json_data,
                                    content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(3, UserWishes.objects.all().count())

    def test_delete_user_wishes(self):
        url = reverse('user_wishes-detail', args=(self.wishes_1.id,))
        self.client.force_login(self.user_1)
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(1, UserWishes.objects.all().count())

    def test_get_ratings(self):
        url = reverse('rating-list')
        response = self.client.get(url)
        test_data = RatingSerializer([self.star_1, self.star_2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(test_data, response.data.get('results'))

    def test_create_rating(self):
        self.assertEqual(2, Rating.objects.all().count())
        data = {
            'star': 2,
            'movie': 2,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user_1)
        response = self.client.post('/api/v1/add_rating/', data=json_data,
                                    content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(3, Rating.objects.all().count())

    def test_create_review(self):
        self.assertEqual(3, Review.objects.all().count())
        data = {
            "email": "test@mail.ua",
            "name": "ilya_test",
            "text": "Comment in test",
            "movie": self.movie_1.id,
            "parent": self.review_1.id
        }

        json_data = json.dumps(data)
        self.client.force_login(self.user_1)
        response = self.client.post('/api/v1/create_review/', data=json_data,
                                    content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4, Review.objects.all().count())
