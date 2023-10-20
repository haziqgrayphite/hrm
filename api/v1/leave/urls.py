from django.urls import path
from .views import (
   LeaveRequestView,
   LeaveRequestTLUpdate,
   LeaveRequestHRUpdate,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/leave-requests/', LeaveRequestView.as_view(), name='leave-request-post'),
    path('api/leave-request/<int:leave_request_id>/', LeaveRequestView.as_view(), name='leave-request-detail'),


    path(
        'api/leave-request-tl-update/<int:leave_request_tl_id>/',
        LeaveRequestTLUpdate.as_view(),
        name='leave-request-tl-update'
    ),

    path(
        'api/leave-request-hr-update/<int:leave_request_hr_id>/',
        LeaveRequestHRUpdate.as_view(),
        name='leave-request-hr-update'
    ),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]
