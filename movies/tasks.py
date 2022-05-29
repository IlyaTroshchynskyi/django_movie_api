"""
    Collect celery tasks
"""


import os

import requests

from django_movie.celery import app
from movies.models import MovieImdb


def get_popular_movie() -> dict:
    """
    Get movies using api
    :return: response
    """

    api_key = os.environ.get('API_KEY', '')
    url = 'https://api.themoviedb.org/3/trending/all/day?api_key=' + api_key\
          + '&language=en-US'
    resp = requests.get(url)
    return resp.json()


def add_movie_to_db(movies: dict) -> None:
    """
    Add movies to db
    :param movies:
    :return:
    """
    for movie in movies.get('results', []):
        movie_id = movie.get('id')
        if not MovieImdb.objects.filter(unique_id=movie_id).exists():

            title = movie.get('title')
            if title:
                overview = movie.get('overview')
                release_date = movie.get('release_date')
                vote_count = movie.get('vote_count', 0)
                vote_average = movie.get('vote_average', 0)
                media_type = movie.get('media_type', 'Unknown')
                record = MovieImdb(unique_id=movie_id,
                                   title=title,
                                   overview=overview,
                                   release_date=release_date,
                                   vote_count=vote_count,
                                   vote_average=vote_average,
                                   media_type=media_type)

                record.save()


@app.task
def send_notification_email(list_films: list):
    """
    Send notification email when film was updated and user was
    subscribed on this film
    :param list_films:
    :return:
    """
    for film in list_films:
        # send_mail('Notification',
        #     f'The movie: "{film.get("movie").get("title")}" was
        #     updated to which you were subscribed',
        #     settings.EMAIL_HOST_USER,  # from_email
        #     [film.get("user").get("email")],  # to_email
        #     fail_silently=False,
        # )
        print(f'Notification {film.get("movie").get("title")}:'
              f'{film.get("user").get("email")}')
    return 'Emails were send'


@app.task
def upload_popular_movies():
    """
    Task for uploading movies to db
    :return:
    """

    data = get_popular_movie()
    add_movie_to_db(data)
    return True
