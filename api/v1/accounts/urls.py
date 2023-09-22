from django.urls import path
from .views import UserApiView, GoogleLoginView, ToBeEvaluatedListView


urlpatterns = [
    path('', UserApiView.as_view(), name='user-list'),
    path('<int:pk>/', UserApiView.as_view(), name='user-detail'),
    path('create/', UserApiView.as_view(), name='user-create'),
    path('<int:pk>/update/', UserApiView.as_view(), name='user-update'),
    path('<int:pk>/patch/', UserApiView.as_view(), name='user-patch'),
    path('<int:pk>/delete/', UserApiView.as_view(), name='user-delete'),
    path('api/google-login/', GoogleLoginView.as_view(), name='facebook_login'),

    path('eval', ToBeEvaluatedListView.as_view(), name='evaluation-detail')


]
