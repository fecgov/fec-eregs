from .base import *

DEBUG = True

# Analytics settings

CACHES['default']['BACKEND'] = 'django.core.cache.backends.dummy.DummyCache'
CACHES['eregs_longterm_cache']['BACKEND'] = 'django.core.cache.backends.dummy.DummyCache'
CACHES['api_cache']['TIMEOUT'] = 5  # roughly per request

# Override the runner from regcore
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

try:
    from local_settings import *
except ImportError:
    pass
