import os
import django
from django.urls import get_resolver

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

resolver = get_resolver()
def print_urls(urllist, prefix=''):
    for entry in urllist:
        if hasattr(entry, 'url_patterns'):
            print_urls(entry.url_patterns, prefix + str(entry.pattern))
        else:
            print(prefix + str(entry.pattern))

print_urls(resolver.url_patterns)
