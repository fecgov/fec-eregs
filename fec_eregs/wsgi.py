import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fec_eregs.settings.prod")

# important that the whitenoise import is after the line above
from whitenoise import WhiteNoise
from django.conf import settings

# This is a work-around because whitenoise does not support SCRIPT_NAME.
# https://github.com/evansd/whitenoise/issues/88
#
# We munge the prefix just enough that it works. Using the Django
# WhiteNoiseMiddleware doesn't give us enough flexibility to get the behavior
# we need.
application = WhiteNoise(
    get_wsgi_application(),
    root=settings.STATIC_ROOT,
    prefix='/static/'
)
