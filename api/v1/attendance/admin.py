from django.contrib import admin
from .models import Attendance, PublicHoliday


class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('attendance_user_id', 'check_in', 'check_out')


class PublicHolidayAdmin(admin.ModelAdmin):
    list_display = ('date', 'name', 'description')


admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(PublicHoliday, PublicHolidayAdmin)
