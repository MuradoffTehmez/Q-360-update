"""
Leave & Attendance Module Serializers.
"""
from rest_framework import serializers
from .models import LeaveRequest, Attendance, LeaveBalance, LeaveType, Holiday
from apps.accounts.models import User


class LeaveTypeSerializer(serializers.ModelSerializer):
    """Serializer for LeaveType model."""

    class Meta:
        model = LeaveType
        fields = [
            'id', 'name', 'code', 'days_per_year', 'requires_approval',
            'is_paid', 'description', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class LeaveRequestSerializer(serializers.ModelSerializer):
    """Serializer for LeaveRequest model."""
    employee_name = serializers.CharField(source='user.get_full_name', read_only=True)
    leave_type_name = serializers.CharField(source='leave_type.name', read_only=True)
    approved_by_name = serializers.CharField(source='approved_by.get_full_name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    number_of_days = serializers.DecimalField(max_digits=5, decimal_places=1, read_only=True)

    class Meta:
        model = LeaveRequest
        fields = [
            'id', 'user', 'employee_name', 'leave_type', 'leave_type_name',
            'start_date', 'end_date', 'number_of_days', 'reason', 'status',
            'status_display', 'approved_by', 'approved_by_name', 'approved_at',
            'rejection_reason', 'created_at', 'updated_at'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at', 'approved_by', 'approved_at']

    def validate(self, data):
        """Validate leave request dates."""
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError({
                'end_date': 'End date must be after start date.'
            })
        return data


class AttendanceSerializer(serializers.ModelSerializer):
    """Serializer for Attendance model."""
    employee_name = serializers.CharField(source='user.get_full_name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    work_hours = serializers.DecimalField(max_digits=4, decimal_places=2, read_only=True)

    class Meta:
        model = Attendance
        fields = [
            'id', 'user', 'employee_name', 'date', 'check_in',
            'check_out', 'work_hours', 'status', 'status_display',
            'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at', 'work_hours']


class LeaveBalanceSerializer(serializers.ModelSerializer):
    """Serializer for LeaveBalance model."""
    employee_name = serializers.CharField(source='user.get_full_name', read_only=True)
    leave_type_name = serializers.CharField(source='leave_type.name', read_only=True)
    available_days = serializers.DecimalField(max_digits=5, decimal_places=1, read_only=True)

    class Meta:
        model = LeaveBalance
        fields = [
            'id', 'user', 'employee_name', 'leave_type', 'leave_type_name',
            'year', 'entitled_days', 'used_days', 'available_days',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at', 'available_days']


class HolidaySerializer(serializers.ModelSerializer):
    """Serializer for Holiday model."""

    class Meta:
        model = Holiday
        fields = [
            'id', 'name', 'date', 'is_recurring', 'description',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
