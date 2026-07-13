from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

from .models import SystemKPI, DashboardWidget, AnalyticsReport, TrendData, ForecastData, RealTimeStat
from .serializers import (
    SystemKPISerializer, DashboardWidgetSerializer, AnalyticsReportSerializer,
    TrendDataSerializer, ForecastDataSerializer, RealTimeStatSerializer
)

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class SystemKPIViewSet(viewsets.ModelViewSet):
    queryset = SystemKPI.objects.all().order_by('-created_at')
    serializer_class = SystemKPISerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['kpi_type']
    search_fields = ['name']

class DashboardWidgetViewSet(viewsets.ModelViewSet):
    queryset = DashboardWidget.objects.all().order_by('order')
    serializer_class = DashboardWidgetSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['widget_type', 'is_active']
    search_fields = ['name', 'title']

class AnalyticsReportViewSet(viewsets.ModelViewSet):
    queryset = AnalyticsReport.objects.all().order_by('-created_at')
    serializer_class = AnalyticsReportSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['report_type', 'is_published']
    search_fields = ['name']

class TrendDataViewSet(viewsets.ModelViewSet):
    queryset = TrendData.objects.all().order_by('-period')
    serializer_class = TrendDataSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['data_type', 'department', 'organization']

class ForecastDataViewSet(viewsets.ModelViewSet):
    queryset = ForecastData.objects.all().order_by('-forecast_date')
    serializer_class = ForecastDataSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['forecast_type', 'department', 'organization']

class RealTimeStatViewSet(viewsets.ModelViewSet):
    queryset = RealTimeStat.objects.all().order_by('stat_type')
    serializer_class = RealTimeStatSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['stat_type', 'organization']
