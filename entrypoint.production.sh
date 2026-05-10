#!/bin/sh
set -e

export FLASK_APP=wsgi

echo "Waiting for database..."
until flask db upgrade; do
  echo "Database not ready, retrying in 2s..."
  sleep 2
done

echo "Copying static files..."
cp -r /home/app/src/static/. /static/

echo "Starting production server..."
exec gunicorn -c src/configs/gunicorn_config.py wsgi:app