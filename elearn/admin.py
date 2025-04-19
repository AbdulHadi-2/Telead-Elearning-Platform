from django.contrib import admin
from django.contrib.auth.models import Group
from allauth.account.models import EmailAddress
from rest_framework.authtoken.models import Token
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialAccount, SocialApp, SocialToken

# Unregister models to hide them from admin
admin.site.unregister(Group)
admin.site.unregister(EmailAddress)
admin.site.unregister(Token)
admin.site.unregister(Site)
admin.site.unregister(SocialAccount)
admin.site.unregister(SocialApp)
admin.site.unregister(SocialToken)

from django.contrib import admin
from django.contrib.admin.sites import AdminSite

# أنشئ نسخة مخصصة من لوحة التحكم
class MyAdminSite(AdminSite):
    def each_context(self, request):
        context = super().each_context(request)
        context['has_permission'] = self.has_permission(request)
        # نحذف recent actions من السياق
        if 'site_title' in context:
            context['site_title'] = 'Telead Admin'
        if 'site_header' in context:
            context['site_header'] = 'Telead Admin'
        return context

    def index(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}
        extra_context['recent_actions'] = []  # نحذفها من الصفحة
        return super().index(request, extra_context=extra_context)

# سجل admin site الجديد
admin_site = MyAdminSite(name='myadmin')