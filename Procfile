release: python3 manage.py migrate;python3 manage.py collectstatic --no-input
web: gunicorn wger.wsgi --log-file -
