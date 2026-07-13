from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

from .models import DevelopmentGoal, ProgressLog
from .models_okr import StrategicObjective, KeyResult, KPI, KPIMeasurement
from .serializers import (
    DevelopmentGoalSerializer, ProgressLogSerializer,
    StrategicObjectiveSerializer, KeyResultSerializer,
    KPISerializer, KPIMeasurementSerializer
)

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class DevelopmentGoalViewSet(viewsets.ModelViewSet):
    queryset = DevelopmentGoal.objects.all().order_by('-created_at')
    serializer_class = DevelopmentGoalSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'category', 'goal_level', 'user', 'related_department']
    search_fields = ['title', 'description']

class ProgressLogViewSet(viewsets.ModelViewSet):
    queryset = ProgressLog.objects.all().order_by('-created_at')
    serializer_class = ProgressLogSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['goal', 'is_draft']

class StrategicObjectiveViewSet(viewsets.ModelViewSet):
    queryset = StrategicObjective.objects.all()
    serializer_class = StrategicObjectiveSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'department', 'owner']
    search_fields = ['title', 'description']

class KeyResultViewSet(viewsets.ModelViewSet):
    queryset = KeyResult.objects.all()
    serializer_class = KeyResultSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['objective']

class KPIViewSet(viewsets.ModelViewSet):
    queryset = KPI.objects.all()
    serializer_class = KPISerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['department', 'owner']
    search_fields = ['name']

class KPIMeasurementViewSet(viewsets.ModelViewSet):
    queryset = KPIMeasurement.objects.all().order_by('-measurement_date')
    serializer_class = KPIMeasurementSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['kpi']
