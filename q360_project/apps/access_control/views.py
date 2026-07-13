from rest_framework import viewsets
from .models import Role, Permission, AbacPolicy
from .serializers import RoleSerializer, PermissionSerializer, AbacPolicySerializer
from .permissions import IsRbacAuthorized

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsRbacAuthorized]
    required_permission = 'role:manage'

class PermissionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsRbacAuthorized]
    required_permission = 'permission:view'

class AbacPolicyViewSet(viewsets.ModelViewSet):
    queryset = AbacPolicy.objects.filter(is_deleted=False)
    serializer_class = AbacPolicySerializer
    permission_classes = [IsRbacAuthorized]
    required_permission = 'abac:manage'
