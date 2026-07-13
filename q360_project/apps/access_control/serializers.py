from rest_framework import serializers
from .models import Role, Permission, RolePermission, UserRole, AbacPolicy

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'

class AbacPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = AbacPolicy
        fields = '__all__'
