from rest_framework import serializers
from .models import SentimentFeedback, SentimentAnalysisSettings

class SentimentFeedbackSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    resolved_by_name = serializers.CharField(source='resolved_by.username', read_only=True)
    
    class Meta:
        model = SentimentFeedback
        fields = '__all__'

class SentimentAnalysisSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SentimentAnalysisSettings
        fields = '__all__'
