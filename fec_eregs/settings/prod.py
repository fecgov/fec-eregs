import json
import os

import dj_database_url
from cfenv import AppEnv

from .base import *

env = AppEnv()

DEBUG = False
TEMPLATE_DEBUG = False
ANALYTICS = {
}

DATABASES = {
    'default': dj_database_url.config()
}


vcap_app = json.loads(os.environ.get('VCAP_APPLICATION', '{}'))

# application_uris might contain paths when a route with path is mapped
ALLOWED_HOSTS = ['localhost'] + [uri.split('/', 1)[0] for uri in vcap_app.get('application_uris', [])]

vcap_services = json.loads(os.environ.get('VCAP_SERVICES', '{}'))
es_config = vcap_services.get('elasticsearch-swarm-1.7.1', [])
if es_config:
    HAYSTACK_CONNECTIONS['default'] = {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': es_config[0]['credentials']['uri'],
        'INDEX_NAME': 'eregs',
    }

HTTP_AUTH_USER = env.get_credential('HTTP_AUTH_USER')
HTTP_AUTH_PASSWORD = env.get_credential('HTTP_AUTH_PASSWORD')
