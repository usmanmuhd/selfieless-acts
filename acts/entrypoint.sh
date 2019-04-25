#!/bin/sh
python3 acts/manage.py migrate
python3 acts/manage.py runserver 0:80
