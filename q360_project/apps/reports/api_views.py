from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

from .models import (
    Report, RadarChartData, ReportGenerationLog, SystemKPI,
    ReportBlueprint, ReportVisualization, CustomReport,
    ReportSchedule, ReportScheduleLog
)
from .serializers import (
    ReportSerializer, RadarChartDataSerializer, ReportGenerationLogSerializer,
    SystemKPISerializer, ReportBlueprintSerializer, ReportVisualizationSerializer,
    CustomReportSerializer, ReportScheduleSerializer, ReportScheduleLogSerializer
)

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all().order_by('-created_at')
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['report_type', 'campaign', 'generated_for']
    search_fields = ['title']

class RadarChartDataViewSet(viewsets.ModelViewSet):
    queryset = RadarChartData.objects.all().order_by('-created_at')
    serializer_class = RadarChartDataSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user', 'campaign', 'category']

class ReportGenerationLogViewSet(viewsets.ModelViewSet):
    queryset = ReportGenerationLog.objects.all().order_by('-created_at')
    serializer_class = ReportGenerationLogSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'report_type', 'requested_by']

class SystemKPIViewSet(viewsets.ModelViewSet):
    queryset = SystemKPI.objects.all().order_by('-date')
    serializer_class = SystemKPISerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['date']

class ReportBlueprintViewSet(viewsets.ModelViewSet):
    queryset = ReportBlueprint.objects.all().order_by('title')
    serializer_class = ReportBlueprintSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['data_source', 'is_active', 'is_global']
    search_fields = ['title', 'description']

class ReportVisualizationViewSet(viewsets.ModelViewSet):
    queryset = ReportVisualization.objects.all().order_by('order')
    serializer_class = ReportVisualizationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['blueprint', 'chart_type']

class CustomReportViewSet(viewsets.ModelViewSet):
    queryset = CustomReport.objects.all().order_by('-created_at')
    serializer_class = CustomReportSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['owner', 'is_active', 'blueprint']
    search_fields = ['name']

class ReportScheduleViewSet(viewsets.ModelViewSet):
    queryset = ReportSchedule.objects.all().order_by('-created_at')
    serializer_class = ReportScheduleSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['frequency', 'is_active', 'created_by']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class ReportScheduleLogViewSet(viewsets.ModelViewSet):
    queryset = ReportScheduleLog.objects.all().order_by('-triggered_at')
    serializer_class = ReportScheduleLogSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'schedule']
