from django.contrib import admin
from django.urls import path, include, re_path

urlpatterns = [
    path('users/', include('api.v1.accounts.urls')),
    path("accounts/", include("allauth.urls")),

]
