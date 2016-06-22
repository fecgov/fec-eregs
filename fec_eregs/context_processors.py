"""
Defines Django context processors specific to fec_eregs.
"""

from django.conf import settings as settings


def app_urls(request):
    return {
        'FEC_API_KEY': settings.FEC_API_KEY,
        'FEC_API_URL': settings.FEC_API_URL,
        'FEC_API_VERSION': settings.FEC_API_VERSION,
        'FEC_CMS_URL': settings.FEC_CMS_URL,
        'FEC_WEB_URL': settings.FEC_WEB_URL,
    }
