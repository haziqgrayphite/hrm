from django.db import models
from enum import Enum
from django.contrib.auth import get_user_model

User = get_user_model()


class AttendanceStatus(Enum):
    PRESENT = 'Present'
    ABSENT = 'Absent'
    AMBIGUOUS = 'Ambiguous'
    ON_LEAVE = 'On Leave'
    WORK_FROM_HOME = 'Work from Home'


class Attendance(models.Model):
    attendance_user_id = models.IntegerField()
    check_in = models.DateTimeField(null=True, blank=True)
    check_out = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[(status.name, status.value) for status in AttendanceStatus],
        default=AttendanceStatus.PRESENT.value
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Attendance for {self.attendance_user_id} at {self.check_in} "


class PublicHoliday(models.Model):
    date = models.DateField()
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


# class Attendee(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendees')
#     email = models.EmailField()
#     attendance_user_id = models.IntegerField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return self.user.username
