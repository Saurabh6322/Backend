import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from allauth.socialaccount.models import SocialAccount, SocialApp
from django.contrib.auth.models import User

print("---- Diagnostics ----")

try:
    sourabh5 = User.objects.get(username="sourabh5")
    accounts = SocialAccount.objects.filter(user=sourabh5)
    print("User sourabh5 connected social accounts:", list(accounts.values('provider', 'uid')))
except User.DoesNotExist:
    print("User sourabh5 does not exist. The message was from something else.")

google_app = SocialApp.objects.filter(provider="google").first()
if google_app:
    print(f"Google App configured correctly? Client ID: {google_app.client_id[:10]}... Secret: {'Set' if google_app.secret else 'Empty'}")
else:
    print("Google App NOT found!")
