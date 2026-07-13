from rest_framework import serializers
from .models import SystemKPI, DashboardWidget, AnalyticsReport, TrendData, ForecastData, RealTimeStat

class SystemKPISerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemKPI
        fields = '__all__'

class DashboardWidgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DashboardWidget
        fields = '__all__'

class AnalyticsReportSerializer(serializers.ModelSerializer):
    generated_by_name = serializers.CharField(source='generated_by.username', read_only=True)

    class Meta:
        model = AnalyticsReport
        fields = '__all__'

class TrendDataSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    organization_name = serializers.CharField(source='organization.name', read_only=True)

    class Meta:
        model = TrendData
        fields = '__all__'

class ForecastDataSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    organization_name = serializers.CharField(source='organization.name', read_only=True)

    class Meta:
        model = ForecastData
        fields = '__all__'

class RealTimeStatSerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(source='organization.name', read_only=True)

    class Meta:
        model = RealTimeStat
        fields = '__all__'
