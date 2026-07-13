from rest_framework import serializers
from .models import FeatureFlag, FeatureFlagRule

class FeatureFlagRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeatureFlagRule
        fields = '__all__'

class FeatureFlagSerializer(serializers.ModelSerializer):
    rules = FeatureFlagRuleSerializer(many=True, read_only=True)
    
    class Meta:
        model = FeatureFlag
        fields = '__all__'
