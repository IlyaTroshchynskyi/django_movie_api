from django.core.management.base import BaseCommand
from movies.models import Category, Genre, Movie, Actor, Rating, RatingStar, \
    Review, Director


class Command(BaseCommand):
    help = 'Seed db'

    def _seed_db(self):
        category_1 = Category.objects.create(name='A', description='First Cat',
                                             url='A')
        category_2 = Category.objects.create(name='B', description='Second Cat',
                                             url='B')
        category_3 = Category.objects.create(name='C', description='Third Cat',
                                             url='C')

        actor_1 = Actor.objects.create(name='Джейсо Стетхем', age=40,
                                       description='Описание')
        actor_2 = Actor.objects.create(name='Джейсо Стетхем2', age=42,
                                       description='Описание')
        actor_3 = Actor.objects.create(name='Джейсо Стетхем3', age=43,
                                       description='Описание')
        actor_4 = Actor.objects.create(name='Джейсо Стетхеv4', age=44,
                                       description='Описание')
        actor_5 = Actor.objects.create(name='Джейсо Стетхем5', age=45,
                                       description='Описание')

        genre_1 = Genre.objects.create(name='Боевик', description='Боевик',
                                       url='Боевик')
        genre_2 = Genre.objects.create(name='Вестерн', description='Вестерн',
                                       url='Вестерн')
        genre_3 = Genre.objects.create(name='Детектив', description='Детектив',
                                       url='Детектив')
        genre_4 = Genre.objects.create(name='Драма', description='Драма',
                                       url='Драма')
        genre_5 = Genre.objects.create(name='Комедия', description='Комедия',
                                       url='Комедия')

        director_1 = Director.objects.create(name='Director1', age=40)
        director_2 = Director.objects.create(name='Director2', age=42)

        film_1 = Movie.objects.create(title='Форсаж1', description='Форсаж1',
                                      year=2019, country='США', budget=100,
                                      fees_is_usa=150, fees_in_world=200,
                                      category=category_1, url='форсаж1')

        film_2 = Movie.objects.create(title='Форсаж2', description='Форсаж2',
                                      year=2019, country='США',
                                      budget=100, fees_is_usa=150, fees_in_world=200,
                                      category=category_2, url='форсаж2')

        film_3 = Movie.objects.create(title='Форсаж3', description='Форсаж3',
                                      year=2019, country='США',
                                      budget=100, fees_is_usa=150, fees_in_world=200,
                                      category=category_3, url='форсаж3')

        film_1.directors.add(director_1)
        film_1.actors.add(actor_1)
        film_1.genres.add(genre_1)

        star_1 = RatingStar.objects.create(value=1)
        star_2 = RatingStar.objects.create(value=2)
        star_3 = RatingStar.objects.create(value=3)
        star_4 = RatingStar.objects.create(value=4)
        star_5 = RatingStar.objects.create(value=5)

        rating_1 = Rating.objects.create(ip='1.1.1.1', star=star_1, movie=film_1)
        rating_2 = Rating.objects.create(ip='2.1.1.1', star=star_2, movie=film_3)
        rating_3 = Rating.objects.create(ip='3.1.1.1', star=star_3, movie=film_2)

        review_1 = Review.objects.create(email='test1@mail.ru', name='Carl',
                                         text='Good film', movie=film_1)
        review_2 = Review.objects.create(email='test1@mail.ru', name='Carl',
                                         text='Good film', parent=review_1,
                                         movie=film_1)
        review_3 = Review.objects.create(email='test2@mail.ru', name='Carl1',
                                         text='Good film', movie=film_3)

    def handle(self, *args, **options):
        self._seed_db()
