#!/bin/bash
echo "Esperando a que PostgreSQL esté listo..."
while ! nc -z db 5432; do
  sleep 1
done
echo "PostgreSQL está listo."

echo "Aplicando migraciones..."
python manage.py migrate

echo "Recopilando archivos estáticos..."
python manage.py collectstatic --noinput

echo "Iniciando Gunicorn..."
exec gunicorn --bind 0.0.0.0:8000 mi_proyecto.wsgi:application
