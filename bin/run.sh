#!/bin/bash

# Set environment options to exit immediately if a non-zero status code
# appears from a command or within a pipe
set -o errexit
set -o pipefail

python manage.py migrate --fake-initial
gunicorn -k gevent -w 2 --bind=0.0.0.0:$PORT fec_eregs.wsgi:application
