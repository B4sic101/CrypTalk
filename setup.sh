#!/bin/sh
sudo apt install python3.12-venv -y
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential pkg-config -y
python3 -m venv venv
source venv/bin/activate
./venv/bin/pip install Django djangorestframework Pillow
./venv/bin/pip -m pip install -U 'channels[daphne]'
./venv/bin/pip install mysql-server PyMySQL
sudo systemctl start mysql
sudo mysql -p -e "create database newdb;" 
./venv/bin/python manage.py makemigrations
./venv/bin/python manage.py makemigrations src
./venv/bin/python manage.py migrate src
./venv/bin/python manage.py migrate
./venv/bin/python manage.py runserver