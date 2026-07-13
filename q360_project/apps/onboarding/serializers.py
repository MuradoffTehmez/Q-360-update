from rest_framework import serializers
from .models import (
    OnboardingTemplate, OnboardingTaskTemplate, OnboardingProcess,
    OnboardingTask, OnboardingNote, MarketSalaryBenchmark
)

class OnboardingTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnboardingTemplate
        fields = '__all__'
        read_only_fields = ['slug', 'created_by']

class OnboardingTaskTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnboardingTaskTemplate
        fields = '__all__'

class OnboardingProcessSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.username', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = OnboardingProcess
        fields = '__all__'

class OnboardingTaskSerializer(serializers.ModelSerializer):
    assigned_to_name = serializers.CharField(source='assigned_to.username', read_only=True)
    completed_by_name = serializers.CharField(source='completed_by.username', read_only=True)

    class Meta:
        model = OnboardingTask
        fields = '__all__'

class OnboardingNoteSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = OnboardingNote
        fields = '__all__'

class MarketSalaryBenchmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketSalaryBenchmark
        fields = '__all__'
