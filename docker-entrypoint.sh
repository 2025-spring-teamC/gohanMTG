#!/bin/bash
set -e

mkdir -p /code/nginx/static
chown -R myuser:mygroup /code/nginx/static

echo "Running npm build..."
npm run build

echo "Collecting static files..."
python django/manage.py collectstatic --noinput

echo "Applying database migrations..."
python django/manage.py migrate

# アプリ起動
echo "Starting Gunicorn..."
exec gunicorn gohanMTG.wsgi:application --chdir django --bind 0.0.0.0:8000

exec gosu myuser "$@"