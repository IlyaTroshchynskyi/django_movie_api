# Create project
start_proj:
    django-admin startproject django_movie

# Create new app inside all project
cr_app:
    ./manage.py startapp movies

# Create migrations
migrate:
    ./manage.py migrate

migrate_doc:
    sudo docker-compose exec web python manage.py migrate

connect_db:
    sudo docker-compose exec db psql --username=ilya --dbname=movie

run:
    ./manage.py runserver

# Create createsuperuser
cr_sup:
    ./manage.py createsuperuser

mm:
    sudo docker-compose exec web python manage.py makemigrations

seed_db:
    sudo docker-compose exec web python manage.py populate_db

run_tests:
    sudo docker-compose exec web python manage.py test movies.tests

# Run celery worker
run_cel:
    sudo docker-compose exec web celery -A django_movie worker -l INFO


run_redis:
    sudo docker run -d -p 6379:6379 redis

run_flower:
    flower -A exchange --port=5555