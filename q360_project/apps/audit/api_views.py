from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

from .models import AuditLog, BlockedIP
from .serializers import AuditLogSerializer, BlockedIPSerializer

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows audit logs to be viewed.
    """
    queryset = AuditLog.objects.all().order_by('-created_at')
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['action', 'severity', 'threat_level', 'model_name']
    search_fields = ['user__username', 'ip_address', 'changes']
    ordering_fields = ['created_at', 'threat_score']

class BlockedIPViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows blocked IPs to be viewed or edited.
    """
    queryset = BlockedIP.objects.all().order_by('-created_at')
    serializer_class = BlockedIPSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['ip_address']
    search_fields = ['ip_address', 'reason']
