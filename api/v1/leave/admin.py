from django.contrib import admin
from .models import (
    SickLeave,
    AnnualLeave,
    CasualLeave,
    LeaveBalance,
    Team,
    TeamLead,
    TeamTitle,
    LeaveRequest,
    LeaveRequestTL,
    LeaveRequestHR
)


class SickLeaveAdmin(admin.ModelAdmin):
    list_display = [
        'leave_type',
        'quota',
        'is_expired',
        'year',
        'expiry_days'
    ]


class AnnualLeaveAdmin(admin.ModelAdmin):
    list_display = [
        'leave_type',
        'quota',
        'is_expired',
        'year',
        'expiry_days'
    ]


class CasualLeaveAdmin(admin.ModelAdmin):
    list_display = [
        'leave_type',
        'quota',
        'is_expired',
        'year',
        'expiry_days'
    ]


class LeaveBalanceAdmin(admin.ModelAdmin):
    list_display = [
        'employee',
        'sick_leave',
        'annual_leave',
        'casual_leave',
        'sick_leave_balance',
        'annual_leave_balance',
        'casual_leave_balance',
        'accumulative_balance'
    ]


class TeamAdmin(admin.ModelAdmin):
    list_display = [
        'member',
        'team_lead',
        'team_title'
    ]


class TeamLeadAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'description'
    ]


class TeamTitleAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'description'
    ]


class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'sick_leave',
        'annual_leave',
        'casual_leave',
        'leave_duration',
        'leaves_required',
        'is_expired',
        'is_team_lead_approval',
        'is_hr_approval',
        'description',
        'status',
        'created_at',
        'updated_at',
        'start_date',
        'end_date'
    ]


class LeaveRequestTLAdmin(admin.ModelAdmin):
    list_display = [
        'leave_request',
        'tl_comments',
        'is_team_lead_approval'
    ]


class LeaveRequestHRAdmin(admin.ModelAdmin):
    list_display = [
        'leave_request',
        'hr_comments',
        'is_hr_approval'
    ]


admin.site.register(SickLeave, SickLeaveAdmin)
admin.site.register(AnnualLeave, AnnualLeaveAdmin)
admin.site.register(CasualLeave, CasualLeaveAdmin)
admin.site.register(LeaveBalance, LeaveBalanceAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(TeamLead, TeamLeadAdmin)
admin.site.register(TeamTitle, TeamTitleAdmin)
admin.site.register(LeaveRequest, LeaveRequestAdmin)
admin.site.register(LeaveRequestTL, LeaveRequestTLAdmin)
admin.site.register(LeaveRequestHR, LeaveRequestHRAdmin)
