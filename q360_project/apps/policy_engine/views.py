from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Policy, PolicyVersion
from .serializers import PolicySerializer, PolicyVersionSerializer
from apps.access_control.permissions import IsRbacAuthorized

class PolicyViewSet(viewsets.ModelViewSet):
    queryset = Policy.objects.filter(is_deleted=False)
    serializer_class = PolicySerializer
    permission_classes = [IsRbacAuthorized]
    required_permission = 'policy:manage'

    @action(detail=True, methods=['post'])
    def add_version(self, request, pk=None):
        policy = self.get_object()
        serializer = PolicyVersionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(policy=policy)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class PolicyVersionViewSet(viewsets.ModelViewSet):
    queryset = PolicyVersion.objects.all()
    serializer_class = PolicyVersionSerializer
    permission_classes = [IsRbacAuthorized]
    required_permission = 'policy:manage'

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        version = self.get_object()
        
        # Deactivate all other versions for this policy
        PolicyVersion.objects.filter(policy=version.policy).update(is_active=False)
        
        # Activate this version
        version.is_active = True
        version.save()
        return Response({"detail": "Policy version activated."})
