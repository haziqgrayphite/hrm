from django.urls import path
from .views import UserApiView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('', UserApiView.as_view(), name='user-list'),
    path('<int:pk>/', UserApiView.as_view(), name='user-detail'),
    path('create/', UserApiView.as_view(), name='user-create'),
    path('<int:pk>/update/', UserApiView.as_view(), name='user-update'),
    path('<int:pk>/patch/', UserApiView.as_view(), name='user-patch'),
    path('<int:pk>/delete/', UserApiView.as_view(), name='user-delete'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
