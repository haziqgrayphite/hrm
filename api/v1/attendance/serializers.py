from rest_framework import serializers
from .models import Attendance, Attendee


class AttendanceSerializer(serializers.ModelSerializer):
    check_in = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    check_out = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Attendance
        fields = ['check_in', 'check_out']


class AttendeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendee
        fields = ['user', 'email', 'attendance_user_id']
