import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

try:
    site = Site.objects.get_current()

    providers = ['linkedin_oauth2', 'twitter']
    for provider in providers:
        if not SocialApp.objects.filter(provider=provider).exists():
            app = SocialApp.objects.create(
                provider=provider,
                name=provider.capitalize(),
                client_id='dummy_client_id_for_' + provider,
                secret='dummy_secret_for_' + provider
            )
            app.sites.add(site)
            print(f"Created temporary dummy test app for {provider}")
        else:
            print(f"App for {provider} already exists.")

    print("DB SocialApps populated.")
except Exception as e:
    print("Error:", e)
