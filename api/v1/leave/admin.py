from django.contrib import admin
from .models import LeaveType, LeaveBalance, LeaveRequest, LeaveApproval, Salary, SalaryDeduction, LeaveAdjustment, Team


class LeaveTypeAdmin(admin.ModelAdmin):
    list_display = [
        'leave_type_name',
        'leave_duration'
    ]


class LeaveBalanceAdmin(admin.ModelAdmin):
    list_display = [
        'approvee',
        'count',
        'year',
        'is_expirable',
        'is_expired',
        'expiry_days'
    ]


class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = [
        'get_approvers',
        'approvee',
        'leave_type',
        'start_date',
        'end_date',
        'leaves_required',
        'reason',
        'status',
        'date_submitted'
    ]

    def get_approvers(self, obj):
        approvers = obj.approver.all()
        approvers_names = [approver.username for approver in approvers]
        return approvers_names

    get_approvers.short_description = 'Approvers'


class LeaveApprovalAdmin(admin.ModelAdmin):
    list_display = [
        'leave_request',
        'approval_date',
        'comments',
        'status'
    ]


class SalaryAdmin(admin.ModelAdmin):
    list_display = [
        'approvee',
        'year',
        'monthly_salary'
    ]


class SalaryDeductionAdmin(admin.ModelAdmin):
    list_display = [
        'approvee',
        'salary',
        'year',
        'deduction_amount'
    ]


class LeaveAdjustmentAdmin(admin.ModelAdmin):
    list_display = [
        'leave_request',
        'adjustment_type',
        'adjustment_date',
        'adjustment_amount',
        'status'
    ]


class TeamAdmin(admin.ModelAdmin):
    list_display = [
        'team_name',
        'description',
    ]


admin.site.register(LeaveType, LeaveTypeAdmin)
admin.site.register(LeaveBalance, LeaveBalanceAdmin)
admin.site.register(LeaveRequest, LeaveRequestAdmin)
admin.site.register(LeaveApproval, LeaveApprovalAdmin)
admin.site.register(Salary, SalaryAdmin)
admin.site.register(SalaryDeduction, SalaryDeductionAdmin)
admin.site.register(LeaveAdjustment, LeaveAdjustmentAdmin)
admin.site.register(Team, TeamAdmin)
