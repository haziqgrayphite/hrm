from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('api.v1.accounts.urls')),
    path("accounts/", include("allauth.urls")),
    path("vendor/", include('api.v1.meal.urls')),
    path("", include('api.v1.meal.urls')),
    path('', include('api.v1.evaluation.urls'))
]
