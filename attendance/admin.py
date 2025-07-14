from django.contrib import admin
from .models import Attendance

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("user", "date", "status", "check_in_time", "check_out_time")
    list_filter = ("status", "date", "user__user_type")
    search_fields = ("user__username",)
    date_hierarchy = "date"
