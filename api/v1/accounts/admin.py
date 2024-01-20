from django.contrib import admin
from rest_framework.authtoken.models import TokenProxy
from allauth.account.models import EmailAddress
from django.contrib.auth.models import Group
from allauth.socialaccount.models import SocialApp, SocialToken
from allauth.socialaccount.models import SocialAccount
from django.contrib.sites.models import Site
from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'username',
        'first_name',
        'last_name',
        'email',
        'is_staff',
        'is_active',
        'gender',
        'role',
        'date_joined',
        'created_at',
        'updated_at'
    ]


admin.site.unregister(TokenProxy)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.unregister(EmailAddress)
# admin.site.unregister(Group)
# admin.site.unregister(SocialApp)
# admin.site.unregister(SocialToken)
# admin.site.unregister(SocialAccount)
# admin.site.unregister(Site)
