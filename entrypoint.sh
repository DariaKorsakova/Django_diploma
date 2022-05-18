#! /bin/bash

python manage.py makemigrations --no-input
python manage.py migrate --no-input

python manage.py collectstatic --no-input
python manage.py migrate --no-input
exec gunicorn shop.wsgi:application -b 0.0.0.0:8000 --reload