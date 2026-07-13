from rest_framework import serializers
from .models import (
    WorkflowTemplate, WorkflowStep, WorkflowCondition, 
    WorkflowTransition, WorkflowInstance, WorkflowInstanceStep, 
    WorkflowHistory
)

class WorkflowTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkflowTemplate
        fields = '__all__'

class WorkflowInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkflowInstance
        fields = '__all__'

class WorkflowInstanceStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkflowInstanceStep
        fields = '__all__'

class WorkflowActionSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=['APPROVE', 'REJECT'])
    comments = serializers.CharField(required=False, allow_blank=True)
