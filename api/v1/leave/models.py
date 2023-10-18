from django.db import models
from enum import Enum
from django.contrib.auth import get_user_model

User = get_user_model()


class ApprovalStatus(Enum):
    PENDING = 'Pending'
    APPROVED = 'Approved'
    REJECTED = 'Rejected'


class LeaveDuration(Enum):
    HALF = 'Half-Day Leave'
    FULL = 'Full-Day Leave'


class SickLeave(models.Model):
    leave_type = "Sick Leave"
    quota = models.PositiveIntegerField(default=5)
    is_expired = models.BooleanField(default=False)
    year = models.PositiveIntegerField()
    expiry_days = models.IntegerField(default=365)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.leave_type


class AnnualLeave(models.Model):
    leave_type = "Annual Leave"
    quota = models.PositiveIntegerField(default=10)
    is_expired = models.BooleanField(default=False)
    year = models.PositiveIntegerField()
    expiry_days = models.IntegerField(default=365)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.leave_type


class CasualLeave(models.Model):
    leave_type = "Wedding Leave"
    quota = models.PositiveIntegerField(default=5)
    is_expired = models.BooleanField(default=False)
    year = models.PositiveIntegerField()
    expiry_days = models.IntegerField(default=365)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.leave_type


class LeaveBalance(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leave_balances_employee')
    sick_leave = models.ForeignKey(SickLeave, on_delete=models.CASCADE, related_name='leave_balances_sick_leave')
    annual_leave = models.ForeignKey(AnnualLeave, on_delete=models.CASCADE, related_name='leave_balances_annual_leave')
    casual_leave = models.ForeignKey(CasualLeave, on_delete=models.CASCADE, related_name='leave_balances_casual_leave')

    sick_leave_balance = models.PositiveIntegerField(default=0)
    annual_leave_balance = models.PositiveIntegerField(default=0)
    casual_leave_balance = models.PositiveIntegerField(default=0)
    accumulative_balance = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):

        if self.sick_leave_balance == 0 and self.sick_leave:
            self.sick_leave_balance = self.sick_leave.quota
        if self.annual_leave_balance == 0 and self.annual_leave:
            self.annual_leave_balance = self.annual_leave.quota
        if self.casual_leave_balance == 0 and self.casual_leave:
            self.casual_leave_balance = self.casual_leave.quota

        self.accumulative_balance = self.sick_leave_balance + self.annual_leave_balance + self.casual_leave_balance

        super(LeaveBalance, self).save(*args, **kwargs)

    def __str__(self):
        return f"Leave Balances for {self.employee.username}"


class TeamTitle(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class TeamLead(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='team_lead_user'
    )

    description = models.CharField(max_length=100)

    def __str__(self):
        return f"Team Lead: {self.user.first_name}"


class Team(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE, )
    team_lead = models.ForeignKey(
        TeamLead,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='team_team_lead'
    )

    team_title = models.ForeignKey(TeamTitle, on_delete=models.CASCADE, related_name='team_team_title')

    def __str__(self):
        return f"Team Member: {self.member}"


class LeaveRequest(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="leave_requests_user"
    )

    sick_leave = models.ForeignKey(
        SickLeave,
        on_delete=models.CASCADE,
        related_name="leave_requests_sick_leave",
        blank=True,
        null=True
    )

    annual_leave = models.ForeignKey(
        AnnualLeave,
        on_delete=models.CASCADE,
        related_name="leave_requests_annual_leave",
        blank=True,
        null=True
    )

    casual_leave = models.ForeignKey(
        CasualLeave,
        on_delete=models.CASCADE,
        related_name="leave_requests_casual_leave",
        blank=True,
        null=True
    )

    leave_duration = models.CharField(
        max_length=50,
        choices=[(duration.value, duration.name) for duration in LeaveDuration],
        unique=True
    )
    leaves_required = models.IntegerField()
    is_expired = models.BooleanField(default=False)
    is_team_lead_approval = models.BooleanField(default=False)
    is_hr_approval = models.BooleanField(default=False)
    description = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=[(status.value, status.name) for status in ApprovalStatus],
        default=ApprovalStatus.PENDING.value
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return (
            f"Leave Request by {self.user} ({self.status}): "
            f"{self.leave_duration} from {self.start_date} to {self.end_date}"
        )


class LeaveRequestTL(models.Model):
    user = models.ForeignKey(TeamLead, on_delete=models.CASCADE, related_name="leave_request_tl_user")
    leave_request = models.ForeignKey(
        LeaveRequest,
        on_delete=models.CASCADE,
        related_name="leave_request_tl_leave_request"
    )

    tl_comments = models.TextField()
    is_team_lead_approval = models.BooleanField(default=False)

    def __str__(self):
        return f"Team Lead Approval for {self.leave_request}"


class LeaveRequestHR(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="leave_request_hr_user")
    leave_request = models.ForeignKey(
        LeaveRequest,
        on_delete=models.CASCADE,
        related_name="leave_request_hr_leave_request"
    )

    hr_comments = models.TextField()
    is_hr_approval = models.BooleanField(default=False)

    def __str__(self):
        return f"HR Approval for {self.leave_request}"
