from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('api.v1.accounts.urls')),
    path("accounts/", include("allauth.urls")),

]
