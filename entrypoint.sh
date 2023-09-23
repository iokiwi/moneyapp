#!/bin/sh

# Wait for DB to be ready
while ! nc -z db 3306; do
  echo "Waiting for MySQL Server"
  sleep 2
done

python manage.py migrate
# gunicorn -b 0.0.0.0:8000 moneyapp.wsgi --reload
export DJANGO_SETTINGS_MODULE="moneyapp.settings"
opentelemetry-instrument gunicorn -b 0.0.0.0:8000 moneyapp.wsgi --reload
