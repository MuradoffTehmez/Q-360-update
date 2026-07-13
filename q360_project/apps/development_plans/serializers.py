from rest_framework import serializers
from .models import DevelopmentGoal, ProgressLog
from .models_okr import StrategicObjective, KeyResult, KPI, KPIMeasurement

class DevelopmentGoalSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = DevelopmentGoal
        fields = '__all__'

class ProgressLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgressLog
        fields = '__all__'

class StrategicObjectiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = StrategicObjective
        fields = '__all__'

class KeyResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyResult
        fields = '__all__'

class KPISerializer(serializers.ModelSerializer):
    class Meta:
        model = KPI
        fields = '__all__'

class KPIMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = KPIMeasurement
        fields = '__all__'
