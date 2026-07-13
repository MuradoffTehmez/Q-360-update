from rest_framework import serializers
from .models import SupportTicket, TicketComment

class TicketCommentSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = TicketComment
        fields = '__all__'

class SupportTicketSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.username', read_only=True)
    comments = TicketCommentSerializer(many=True, read_only=True)

    class Meta:
        model = SupportTicket
        fields = '__all__'
