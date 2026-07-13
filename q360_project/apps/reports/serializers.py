from rest_framework import serializers
from .models import (
    Report, RadarChartData, ReportGenerationLog, SystemKPI,
    ReportBlueprint, ReportVisualization, CustomReport,
    ReportSchedule, ReportScheduleLog
)

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'

class RadarChartDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = RadarChartData
        fields = '__all__'

class ReportGenerationLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportGenerationLog
        fields = '__all__'

class SystemKPISerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemKPI
        fields = '__all__'

class ReportBlueprintSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportBlueprint
        fields = '__all__'
        read_only_fields = ['slug']

class ReportVisualizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportVisualization
        fields = '__all__'

class CustomReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomReport
        fields = '__all__'

class ReportScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportSchedule
        fields = '__all__'
        read_only_fields = ['created_by', 'last_run', 'next_run', 'last_status']

class ReportScheduleLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportScheduleLog
        fields = '__all__'
