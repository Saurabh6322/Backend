from rest_framework import serializers
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount

class CustomUserDetailsSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('pk', 'username', 'email', 'first_name', 'last_name', 'avatar_url')
        read_only_fields = ('email', )

    def get_avatar_url(self, obj):
        try:
            # Check if user has a Google SocialAccount
            social_account = SocialAccount.objects.filter(user=obj, provider='google').first()
            if social_account and social_account.extra_data.get('picture'):
                return social_account.extra_data.get('picture')
        except Exception:
            pass
        return None
