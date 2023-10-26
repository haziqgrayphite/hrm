from django.contrib import admin
from .models import Attendance, Attendee


class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('attendance_user_id', 'check_in', 'check_out')


class AttendeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'attendance_user_id', 'email')


admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(Attendee, AttendeeAdmin)
