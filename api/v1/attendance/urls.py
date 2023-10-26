from django.urls import path
from .views import PostAttendanceAPIView, ExcelInsertAPIView, PreviousDayAttendanceAPIView


urlpatterns = [
    path('api/post-attendance/', PostAttendanceAPIView.as_view(), name='post_attendance'),
    path('excel-insert/', ExcelInsertAPIView.as_view(), name='excel-insert'),
    path('api/previous-day-attendance/', PreviousDayAttendanceAPIView.as_view(), name='previous-day-attendance'),
]
