from django.contrib import admin
from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'gender', 'role',
                    'date_joined', 'created_at', 'updated_at']


admin.site.register(CustomUser, CustomUserAdmin)
