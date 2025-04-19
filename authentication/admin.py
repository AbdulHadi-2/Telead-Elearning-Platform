from django.contrib import admin
from django.apps import apps
from .models import *
from django.contrib.auth.models import Group
from allauth.account.models import EmailAddress
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialAccount, SocialApp, SocialToken

app_models = apps.get_app_config('authentication').get_models()
for model in app_models:
    if model.__name__ in ["CustomUser", "Video","Mentor"]:
        admin.site.register(model)
    
    
admin.site.unregister(Group)
admin.site.unregister(EmailAddress)
# admin.site.unregister(Token)
admin.site.unregister(Site)
admin.site.unregister(SocialAccount)
admin.site.unregister(SocialApp)
admin.site.unregister(SocialToken)
