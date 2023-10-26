from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Attendance(models.Model):
    attendance_user_id = models.IntegerField()
    check_in = models.DateTimeField(null=True, blank=True)
    check_out = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Attendance for {self.attendance_user_id} at {self.check_in}"


class Attendee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendees')
    email = models.EmailField()
    attendance_user_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
