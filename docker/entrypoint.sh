#!/bin/bash

echo "Waiting for PostgreSQL to be ready..."
until PGPASSWORD=$DATABASE_PASSWORD psql -h "db" -U "$DATABASE_USER" -d "$DATABASE_NAME" -c '\q'; do
  >&2 echo "PostgreSQL is still unavailable - sleeping"
  sleep 2
done

echo "PostgreSQL is up - applying migrations"

# Apply migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec gunicorn --bind 0.0.0.0:8000 config.wsgi:application

