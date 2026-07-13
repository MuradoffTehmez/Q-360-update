"""
Serializers for performance_reviews app.
"""
from rest_framework import serializers
from .models import ReviewSession, ReviewNote, ReviewActionItem, CompetencyEvaluation
from apps.accounts.models import User


class UserBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'position']


class ReviewNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewNote
        fields = ['id', 'session', 'topic', 'content', 'created_at']
        read_only_fields = ['created_at']


class ReviewActionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewActionItem
        fields = ['id', 'session', 'description', 'due_date', 'is_completed', 'created_at']
        read_only_fields = ['created_at']


class CompetencyEvaluationSerializer(serializers.ModelSerializer):
    competency_name = serializers.CharField(source='competency.name', read_only=True)
    manager_rating_name = serializers.CharField(source='manager_rating.display_name', read_only=True)

    class Meta:
        model = CompetencyEvaluation
        fields = ['id', 'session', 'competency', 'competency_name', 'manager_rating', 'manager_rating_name', 'comment']
        read_only_fields = []


class ReviewSessionListSerializer(serializers.ModelSerializer):
    manager = UserBasicSerializer(read_only=True)
    employee = UserBasicSerializer(read_only=True)

    class Meta:
        model = ReviewSession
        fields = ['id', 'manager', 'employee', 'date', 'status', 'created_at']


class ReviewSessionDetailSerializer(serializers.ModelSerializer):
    manager = UserBasicSerializer(read_only=True)
    employee = UserBasicSerializer(read_only=True)
    notes = ReviewNoteSerializer(many=True, read_only=True)
    action_items = ReviewActionItemSerializer(many=True, read_only=True)
    competency_evaluations = CompetencyEvaluationSerializer(many=True, read_only=True)

    class Meta:
        model = ReviewSession
        fields = [
            'id', 'manager', 'employee', 'date', 'status', 'overall_notes',
            'created_at', 'updated_at', 'notes', 'action_items', 'competency_evaluations'
        ]


class ReviewSessionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewSession
        fields = ['employee', 'date', 'status', 'overall_notes']

    def validate_employee(self, value):
        # Ensure employee is active and not the manager themselves
        request = self.context.get('request')
        if request and request.user == value:
            raise serializers.ValidationError("Özünüzlə 1-on-1 yarada bilməzsiniz.")
        if not value.is_active:
            raise serializers.ValidationError("İşçi aktiv deyil.")
        return value
