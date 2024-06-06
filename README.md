docker-compose run django python manage.py createsuperuser

poetry run python manage.py createsuperuser

docker build -t vkr-django --no-cashe .

docker-compose up [down]

poetry run python manage.py makemigrations
poetry run python manage.py migrate

docker-compose run django python manage.py collectstatic