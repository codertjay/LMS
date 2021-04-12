from django.conf import settings
from django_hosts import patterns, host

host_patterns = patterns(
    '',
    host(r'www', settings.ROOT_URLCONF, name='www'),
    host('', settings.ROOT_URLCONF, name=''),
    host(r'academy', 'Learning_platform.hostsconf.urls', name='academy'),
)


