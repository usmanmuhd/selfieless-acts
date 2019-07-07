#!/bin/sh
python3 acts/manage.py migrate
echo "Starting server!"
python3 acts/manage.py runserver 0:80
