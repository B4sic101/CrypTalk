#!/bin/sh
sudo apt-get install python3.12-venv python3-dev default-libmysqlclient-dev build-essential pkg-config mysql-server -y
python3 -m venv venv
source venv/bin/activate
sudo ./venv/bin/pip install Django djangorestframework Pillow PyMySQL mysqlclient python-dotenv django-extensions channels-redis
sudo ./venv/bin/pip install -U 'channels[daphne]'
sudo systemctl start mysql

sudo mysql -p -e "create database cryptalkdb;" 
sudo apt-get install lsb-release curl gpg
curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg
sudo chmod 644 /usr/share/keyrings/redis-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list
sudo apt-get update
sudo apt-get install redis
sudo systemctl enable redis-server
sudo systemctl start redis-server

sudo ./venv/bin/python manage.py makemigrations api
sudo ./venv/bin/python manage.py makemigrations src
sudo ./venv/bin/python manage.py migrate src
sudo ./venv/bin/python manage.py migrate api
sudo ./venv/bin/python manage.py makemigrations
sudo ./venv/bin/python manage.py migrate
sudo ./venv/bin/python manage.py runserver