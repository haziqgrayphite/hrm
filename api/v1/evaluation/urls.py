from django.urls import path
from .views import GeneralAPIView, PendingEvaluationAPIView, UpdateEvaluationScores, CompletedEvaluationAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('general_data/', GeneralAPIView.as_view(), name='general-api'),
    path('pending-evaluation/', PendingEvaluationAPIView.as_view(), name='evaluation-api'),
    path('completed-evaluation/', CompletedEvaluationAPIView.as_view(), name='evaluation-api'),
    path('update-evaluation-scores/', UpdateEvaluationScores.as_view(), name='update-evaluation-scores'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]
