python manage.py collectstatic --noinput -v 0
python manage.py migrate --fake-initial
gunicorn -k gevent -w 2 --bind=0.0.0.0:$PORT fec_eregs.wsgi:application
