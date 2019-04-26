#!/bin/sh
python3 users/manage.py migrate
python3 users/manage.py runserver 0:80
