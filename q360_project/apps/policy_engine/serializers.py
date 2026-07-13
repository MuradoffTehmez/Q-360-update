from rest_framework import serializers
from .models import Policy, PolicyVersion

class PolicyVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolicyVersion
        fields = '__all__'

class PolicySerializer(serializers.ModelSerializer):
    versions = PolicyVersionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Policy
        fields = '__all__'
