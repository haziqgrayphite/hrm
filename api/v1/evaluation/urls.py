from django.urls import path
from .views import GeneralAPIView, EvaluationAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('general_data/', GeneralAPIView.as_view(), name='general-api'),
    path('evaluation/', EvaluationAPIView.as_view(), name='evaluation-api'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]
