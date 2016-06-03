import json
import os

from cfenv import AppEnv
env = AppEnv()

from regcore.settings.base import *
REGCORE_APPS = tuple(INSTALLED_APPS)
REGCORE_DATABASES = dict(DATABASES)

from regulations.settings.base import *
REGSITE_APPS = tuple(INSTALLED_APPS)

INSTALLED_APPS = ('overextends', 'fec_eregs',) + REGCORE_APPS + REGSITE_APPS

NOSE_ARGS = [
    '--with-coverage',
    '--cover-package=regcore,regulations',
    '--tests=regulations.tests,regcore.tests,fec_eregs/tests/',
    '--verbosity=3'
]

TEMPLATES[0]['OPTIONS']['context_processors'] += (
    'fec_eregs.context_processors.app_urls',
)

TEST_RUNNER = 'django_nose.runner.NoseTestSuiteRunner'

ROOT_URLCONF = 'fec_eregs.urls'

DATABASES = REGCORE_DATABASES

API_BASE = 'http://localhost:{}/api/'.format(
    os.environ.get('VCAP_APP_PORT', '8000'))

STATICFILES_DIRS = ['compiled']

DATA_LAYERS = DATA_LAYERS or []

DATA_LAYERS = DATA_LAYERS + (
    'regulations.generator.layers.external_citation.ExternalCitationLayer',)

FEC_API_KEY = env.get_credential('FEC_API_KEY', '')
FEC_API_VERSION = os.environ.get('FEC_API_VERSION', 'v1')

FEC_API_URL = os.environ.get('FEC_API_URL', '')
FEC_CMS_URL = os.environ.get('FEC_CMS_URL', '')
FEC_WEB_URL = os.environ.get('FEC_WEB_URL', '')
