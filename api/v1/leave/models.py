from django.db import models
from enum import Enum
from api.v1.leave.constants import RoleChoices


class ApprovalStatus(Enum):
    PENDING = 'Pending'
    APPROVED = 'Approved'
    REJECTED = 'Rejected'


class LeaveDuration(Enum):
    HALF = 'Half-Day Leave'
    FULL = 'Full-Day Leave'


class LeaveType(models.Model):
    leave_type_name = models.CharField(max_length=50, unique=True)
    leave_duration = models.CharField(
        max_length=50,
        choices=[(duration.value, duration.name) for duration in LeaveDuration],
        unique=True
    )

    def __str__(self):
        return self.leave_type_name


class LeaveBalance(models.Model):
    approvee = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name="leave_balances")

    is_expirable = models.BooleanField(default=True)
    is_expired = models.BooleanField(default=False)
    count = models.PositiveIntegerField(default=24)
    year = models.PositiveIntegerField()
    expiry_days = models.IntegerField(default=365)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Leave Entitlement - {self.approvee}, Year {self.year}"


class Team(models.Model):
    team_name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.team_name


class LeaveRequest(models.Model):
    team_lead = models.ForeignKey(
        'accounts.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='teams_as_lead',
        limit_choices_to={'role': RoleChoices.TEAM_LEAD.value}
    )
    approvee = models.ForeignKey(
        'accounts.CustomUser',
        on_delete=models.CASCADE,
        related_name="leave_requests_submitted"
    )
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE, related_name="leave_requests_leave_type")

    leaves_required = models.IntegerField()
    is_expirable = models.BooleanField(default=True)
    is_expired = models.BooleanField(default=False)
    reason = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=[(status.value, status.name) for status in ApprovalStatus],
        default=ApprovalStatus.PENDING.value
    )

    date_submitted = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return (
            f"Leave Request by {self.approvee} ({self.status}): "
            f"{self.leave_type} - {self.start_date} to {self.end_date}"
        )


class LeaveApproval(models.Model):
    leave_request = models.ForeignKey(LeaveRequest, on_delete=models.CASCADE, related_name="approvals")

    approval_date = models.DateTimeField(auto_now_add=True)
    comments = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=[(status.value, status.name) for status in ApprovalStatus],
        default=ApprovalStatus.PENDING.value
    )

    def __str__(self):
        return f"Leave Approval for {self.leave_request} , Status: {self.status}"


class AdjustmentType(models.Model):
    adjustment_type_name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.adjustment_type_name


class LeaveAdjustment(models.Model):
    leave_request = models.ForeignKey(
        'LeaveRequest',
        on_delete=models.CASCADE,
        related_name="adjustments_leave_requests"
    )
    adjustment_type = models.ForeignKey(
        AdjustmentType,
        on_delete=models.CASCADE,
        related_name="adjustments_adjustment_type"
    )

    adjustment_date = models.DateField()
    adjustment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[(status.value, status.name) for status in ApprovalStatus],
        default=ApprovalStatus.PENDING.value
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Leave Adjustment for {self.leave_request} on {self.adjustment_date}, Status: {self.status}"


class Salary(models.Model):
    approvee = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name="salaries")

    year = models.PositiveIntegerField()
    monthly_salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Salary for {self.approvee} in {self.year}"


class SalaryDeduction(models.Model):
    approvee = models.ForeignKey(
        'accounts.CustomUser',
        on_delete=models.CASCADE,
        related_name="salary_deduction_approvee"
    )
    salary = models.ForeignKey(Salary, on_delete=models.CASCADE, related_name="deductions")

    year = models.PositiveIntegerField()
    deduction_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Salary Deduction for {self.approvee} in {self.year}"
