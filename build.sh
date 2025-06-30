#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Make new migrations
python manage.py makemigrations --noinput

# Apply database migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput