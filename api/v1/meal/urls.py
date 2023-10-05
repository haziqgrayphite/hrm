from django.urls import path
from .views import VendorAPIView, MealAPIView, MenuAPIView, ReviewAPIView, MealReviewAPIView

urlpatterns = [
    path('', VendorAPIView.as_view(), name='vendor-list'),
    path('<int:pk>/', VendorAPIView.as_view(), name='vendor-detail'),
    path('post/', VendorAPIView.as_view(), name='vendor-post'),
    path('<int:pk>/update/', VendorAPIView.as_view(), name='vendor-update'),
    path('<int:pk>/partial-update/', VendorAPIView.as_view(), name='vendor-partial-update'),
    path('<int:pk>/delete/', VendorAPIView.as_view(), name='vendor-delete'),

    path('meals/', MealAPIView.as_view(), name='meal-list'),
    path('meals/<int:pk>/', MealAPIView.as_view(), name='meal-detail'),
    path('meals/post/', MealAPIView.as_view(), name='meal-post'),
    path('meals/<int:pk>/update/', MealAPIView.as_view(), name='meal-update'),
    path('meals/<int:pk>/partial-update/', MealAPIView.as_view(), name='meal-partial-update'),
    path('meals/<int:pk>/delete/', MealAPIView.as_view(), name='meal-delete'),

    path('menus/', MenuAPIView.as_view(), name='menu-list'),
    path('menus/<int:pk>/', MenuAPIView.as_view(), name='menu-detail'),
    path('menus/post/', MenuAPIView.as_view(), name='menu-post'),
    path('menus/<int:pk>/update/', MenuAPIView.as_view(), name='menu-update'),
    path('menus/<int:pk>/partial-update/', MenuAPIView.as_view(), name='menu-partial-update'),
    path('menus/<int:pk>/delete/', MenuAPIView.as_view(), name='menu-delete'),

    path('reviews/', ReviewAPIView.as_view(), name='review-list'),
    path('reviews/<int:pk>/', ReviewAPIView.as_view(), name='review-detail'),
    path('reviews/post/', ReviewAPIView.as_view(), name='review-post'),
    path('reviews/<int:pk>/update/', ReviewAPIView.as_view(), name='review-update'),
    path('reviews/<int:pk>/partial-update/', ReviewAPIView.as_view(), name='review-partial-update'),
    path('reviews/<int:pk>/delete/', ReviewAPIView.as_view(), name='review-delete'),

    path('meal-reviews/', MealReviewAPIView.as_view(), name='meal-review-list'),
    path('meal-reviews/post/', MealReviewAPIView.as_view(), name='meal-review-post'),
    path('meal-reviews/<int:pk>/', MealReviewAPIView.as_view(), name='meal-review-update'),

]
