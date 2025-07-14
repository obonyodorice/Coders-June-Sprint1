from rest_framework import serializers
from .models import Attendance

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = [
            'id',
            'role',
            'department',
            'check_in_time',
            'check_out_time',
            'status',
            'date'
        ]
        read_only_fields = [
            'id',
            'check_in_time',
            'check_out_time',
            'status',
            'date'
        ]
