from .base import *
import os

DEBUG = True
INSTALLED_APPS = INSTALLED_APPS + ('debug_toolbar',)

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

# Analytics settings

CACHES['default']['BACKEND'] = 'django.core.cache.backends.dummy.DummyCache'
CACHES['eregs_longterm_cache']['BACKEND'] = 'django.core.cache.backends.dummy.DummyCache'
CACHES['api_cache']['TIMEOUT'] = 5  # roughly per request

FEC_API_URL = os.environ.get('FEC_API_URL', 'http://localhost:5000')
FEC_CMS_URL = os.environ.get('FEC_CMS_URL', 'http://localhost:8000')
FEC_WEB_URL = os.environ.get('FEC_WEB_URL', 'http://localhost:3000')

try:
    from local_settings import *
except ImportError:
    pass
