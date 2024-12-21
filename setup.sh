#!/bin/sh
python3 -m venv venv
./venv/bin/pip install Django djangorestframework Pillow
./venv/bin/python manage.py makemigrations src
./venv/bin/python manage.py migrate src
./venv/bin/python manage.py migrate
./venv/bin/python manage.py runserver