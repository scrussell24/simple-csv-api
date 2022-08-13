#!/bin/bash
python manage.py showmigrations
python manage.py makemigrations api
python manage.py migrate