from rest_framework import permissions
from .models import LeaveRequestTL, Team


class IsTeamLeadOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:
            return True

        return self.is_team_lead(request)

    def is_team_lead(self, request):

        leave_request_tl = LeaveRequestTL.objects.get(id=request.parser_context['kwargs']['leave_request_tl_id'])
        requesting_user = request.user
        leave_request_user = leave_request_tl.leave_request.user

        try:
            team_of_leave_request_user = Team.objects.get(member=leave_request_user)

            if team_of_leave_request_user.team_lead and requesting_user == team_of_leave_request_user.team_lead.user:
                return True

        except Team.DoesNotExist:
            pass

        return False
