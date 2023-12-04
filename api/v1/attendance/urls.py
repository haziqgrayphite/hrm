from django.urls import path
from .views import PostAttendanceAPIView, SyncAttendanceAPIView, PreviousMonthAttendanceAPIView


urlpatterns = [
    path('api/post-attendance/', PostAttendanceAPIView.as_view(), name='post_attendance'),
    path('api/sync-attendance/', SyncAttendanceAPIView.as_view(), name='sync-attendance'),
    path('api/get/month-attendance/', PreviousMonthAttendanceAPIView.as_view(), name='previous-day-attendance'),
]
