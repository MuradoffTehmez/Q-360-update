from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

from .models import (
    OnboardingTemplate, OnboardingTaskTemplate, OnboardingProcess,
    OnboardingTask, OnboardingNote, MarketSalaryBenchmark
)
from .serializers import (
    OnboardingTemplateSerializer, OnboardingTaskTemplateSerializer, OnboardingProcessSerializer,
    OnboardingTaskSerializer, OnboardingNoteSerializer, MarketSalaryBenchmarkSerializer
)

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class OnboardingTemplateViewSet(viewsets.ModelViewSet):
    queryset = OnboardingTemplate.objects.all().order_by('name')
    serializer_class = OnboardingTemplateSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_default', 'is_active']
    search_fields = ['name', 'description']

class OnboardingTaskTemplateViewSet(viewsets.ModelViewSet):
    queryset = OnboardingTaskTemplate.objects.all().order_by('order')
    serializer_class = OnboardingTaskTemplateSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['template', 'task_type', 'assignee_role']
    search_fields = ['title', 'description']

class OnboardingProcessViewSet(viewsets.ModelViewSet):
    queryset = OnboardingProcess.objects.all().order_by('-created_at')
    serializer_class = OnboardingProcessSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['employee', 'template', 'department', 'status']

class OnboardingTaskViewSet(viewsets.ModelViewSet):
    queryset = OnboardingTask.objects.all().order_by('due_date')
    serializer_class = OnboardingTaskSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['process', 'task_type', 'assigned_to', 'status']
    search_fields = ['title', 'description']

class OnboardingNoteViewSet(viewsets.ModelViewSet):
    queryset = OnboardingNote.objects.all().order_by('-created_at')
    serializer_class = OnboardingNoteSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['process', 'author']

class MarketSalaryBenchmarkViewSet(viewsets.ModelViewSet):
    queryset = MarketSalaryBenchmark.objects.all().order_by('-effective_date')
    serializer_class = MarketSalaryBenchmarkSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['department', 'role_level']
    search_fields = ['title']
