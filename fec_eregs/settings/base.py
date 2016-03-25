import json
import os

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

TEST_RUNNER = 'django_nose.runner.NoseTestSuiteRunner'

ROOT_URLCONF = 'fec_eregs.urls'

DATABASES = REGCORE_DATABASES

API_BASE = 'http://localhost:{}/api/'.format(
    os.environ.get('VCAP_APP_PORT', '8000'))

STATICFILES_DIRS = ['compiled']
