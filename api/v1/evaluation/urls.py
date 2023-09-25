from django.urls import path
from .views import EvaluationAPIView

urlpatterns = [
    path('evaluations/', EvaluationAPIView.as_view(), name='evaluation-list')
]
