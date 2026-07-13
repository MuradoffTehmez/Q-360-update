"""
Recruitment Module Serializers.
"""
from rest_framework import serializers
from .models import JobPosting, Application, Interview, Offer
from apps.accounts.models import User


class JobPostingSerializer(serializers.ModelSerializer):
    """Serializer for JobPosting model."""
    department_name = serializers.CharField(source='department.name', read_only=True, allow_null=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True, allow_null=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = JobPosting
        fields = [
            'id', 'title', 'department', 'department_name', 'description',
            'requirements', 'responsibilities', 'employment_type', 'location',
            'salary_min', 'salary_max', 'salary_currency', 'status', 'status_display',
            'posted_date', 'closing_date', 'created_by', 'created_by_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'posted_date', 'created_by']


class ApplicationSerializer(serializers.ModelSerializer):
    """Serializer for Application model."""
    job_title = serializers.CharField(source='job_posting.title', read_only=True)
    full_name = serializers.CharField(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Application
        fields = [
            'id', 'job_posting', 'job_title', 'first_name', 'last_name', 'full_name', 'email',
            'phone', 'resume', 'cover_letter', 'status', 'status_display',
            'applied_at', 'notes', 'updated_at'
        ]
        read_only_fields = ['updated_at', 'applied_at']


class InterviewSerializer(serializers.ModelSerializer):
    """Serializer for Interview model."""
    application_info = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Interview
        fields = [
            'id', 'application', 'application_info', 'interview_type',
            'scheduled_date', 'duration_minutes',
            'location', 'interviewers',
            'status', 'status_display', 'feedback', 'rating',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_application_info(self, obj):
        """Get application summary info."""
        return {
            'id': obj.application.id,
            'job_title': obj.application.job_posting.title,
            'full_name': obj.application.full_name,
            'email': obj.application.email
        }


class OfferSerializer(serializers.ModelSerializer):
    """Serializer for Offer model."""
    application_info = serializers.SerializerMethodField()
    approved_by_name = serializers.CharField(source='approved_by.get_full_name', read_only=True, allow_null=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Offer
        fields = [
            'id', 'application', 'application_info', 'salary',
            'currency', 'start_date', 'sent_date', 'expiry_date',
            'status', 'status_display', 'approved_by', 'approved_by_name',
            'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_application_info(self, obj):
        """Get application summary info."""
        return {
            'id': obj.application.id,
            'job_title': obj.application.job_posting.title,
            'full_name': obj.application.full_name
        }
