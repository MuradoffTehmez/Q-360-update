from rest_framework import viewsets
from .models import FeatureFlag, FeatureFlagRule
from .serializers import FeatureFlagSerializer, FeatureFlagRuleSerializer
from apps.access_control.permissions import IsRbacAuthorized

class FeatureFlagViewSet(viewsets.ModelViewSet):
    queryset = FeatureFlag.objects.all()
    serializer_class = FeatureFlagSerializer
    permission_classes = [IsRbacAuthorized]
    required_permission = 'feature_flags:manage'

class FeatureFlagRuleViewSet(viewsets.ModelViewSet):
    queryset = FeatureFlagRule.objects.all()
    serializer_class = FeatureFlagRuleSerializer
    permission_classes = [IsRbacAuthorized]
    required_permission = 'feature_flags:manage'
