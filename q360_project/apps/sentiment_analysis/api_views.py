from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

from .models import SentimentFeedback, SentimentAnalysisSettings
from .serializers import SentimentFeedbackSerializer, SentimentAnalysisSettingsSerializer

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class SentimentFeedbackViewSet(viewsets.ModelViewSet):
    queryset = SentimentFeedback.objects.all().order_by('-created_at')
    serializer_class = SentimentFeedbackSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['sentiment_label', 'is_resolved', 'user', 'resolved_by']
    search_fields = ['feedback_text']

class SentimentAnalysisSettingsViewSet(viewsets.ModelViewSet):
    queryset = SentimentAnalysisSettings.objects.all()
    serializer_class = SentimentAnalysisSettingsSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
