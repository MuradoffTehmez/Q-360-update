from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import (
    NotificationMethod, NotificationTemplate, Notification,
    SMSProvider, SMSLog, SMSNotification,
    PushDevice, PushNotification,
    NotificationPreference, UserNotificationPreference,
    BulkNotification, EmailTemplate, EmailLog, EmailNotification
)
from .serializers import (
    NotificationMethodSerializer, NotificationTemplateSerializer, NotificationSerializer,
    SMSProviderSerializer, SMSLogSerializer, SMSNotificationSerializer,
    PushDeviceSerializer, PushNotificationSerializer,
    NotificationPreferenceSerializer, UserNotificationPreferenceSerializer,
    BulkNotificationSerializer, EmailTemplateSerializer, EmailLogSerializer, EmailNotificationSerializer
)

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class NotificationMethodViewSet(viewsets.ModelViewSet):
    queryset = NotificationMethod.objects.all().order_by('name')
    serializer_class = NotificationMethodSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['method_type', 'is_active']
    search_fields = ['name']

class NotificationTemplateViewSet(viewsets.ModelViewSet):
    queryset = NotificationTemplate.objects.all().order_by('name')
    serializer_class = NotificationTemplateSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['trigger', 'is_active']
    search_fields = ['name', 'subject']

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all().order_by('-created_at')
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['notification_type', 'channel', 'is_read', 'priority', 'user']
    search_fields = ['title', 'message']

    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'is_superuser', False):
            return super().get_queryset()
        return super().get_queryset().filter(user=user)
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        notification = self.get_object()
        notification.mark_as_read()
        return Response({'status': 'marked as read'})

class SMSProviderViewSet(viewsets.ModelViewSet):
    queryset = SMSProvider.objects.all().order_by('name')
    serializer_class = SMSProviderSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['provider', 'is_active']
    search_fields = ['name']

class SMSLogViewSet(viewsets.ModelViewSet):
    queryset = SMSLog.objects.all().order_by('-created_at')
    serializer_class = SMSLogSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'provider']
    search_fields = ['recipient_phone', 'message']

class SMSNotificationViewSet(viewsets.ModelViewSet):
    queryset = SMSNotification.objects.all().order_by('-created_at')
    serializer_class = SMSNotificationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'provider']
    search_fields = ['recipient_phone', 'message']

class PushDeviceViewSet(viewsets.ModelViewSet):
    queryset = PushDevice.objects.all().order_by('-updated_at')
    serializer_class = PushDeviceSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['platform', 'is_active', 'user']
    search_fields = ['name', 'device_token']

class PushNotificationViewSet(viewsets.ModelViewSet):
    queryset = PushNotification.objects.all().order_by('-created_at')
    serializer_class = PushNotificationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'priority']
    search_fields = ['title', 'message']

class NotificationPreferenceViewSet(viewsets.ModelViewSet):
    queryset = NotificationPreference.objects.all()
    serializer_class = NotificationPreferenceSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['method', 'category', 'enabled', 'user']

class UserNotificationPreferenceViewSet(viewsets.ModelViewSet):
    queryset = UserNotificationPreference.objects.all()
    serializer_class = UserNotificationPreferenceSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user']

class BulkNotificationViewSet(viewsets.ModelViewSet):
    queryset = BulkNotification.objects.all().order_by('-created_at')
    serializer_class = BulkNotificationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status']
    search_fields = ['title', 'message']

class EmailTemplateViewSet(viewsets.ModelViewSet):
    queryset = EmailTemplate.objects.all().order_by('name')
    serializer_class = EmailTemplateSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'subject']

class EmailLogViewSet(viewsets.ModelViewSet):
    queryset = EmailLog.objects.all().order_by('-created_at')
    serializer_class = EmailLogSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'template']
    search_fields = ['recipient_email', 'subject']

class EmailNotificationViewSet(viewsets.ModelViewSet):
    queryset = EmailNotification.objects.all().order_by('-created_at')
    serializer_class = EmailNotificationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'priority']
    search_fields = ['recipient_email', 'subject']
