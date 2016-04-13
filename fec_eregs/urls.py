from django.conf.urls import include, url

from regcore import urls as regcore_urls
from regulations import urls as regsite_urls


extra_patterns = [
    url(r'^api/', include(regcore_urls))
] + regsite_urls.urlpatterns

urlpatterns = [
    url(r'^legal-viewer/', include(extra_patterns))
]
