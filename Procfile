web: gunicorn afyalink.wsgi:application --bind 0.0.0.0:$PORT
worker: celery -A afyalink worker --loglevel=info
beat: celery -A afyalink beat --loglevel=info
