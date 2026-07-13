from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from .models import Role, Permission, RolePermission, UserRole, AbacPolicy


class RolePermissionInline(TabularInline):
    model = RolePermission
    extra = 1
    autocomplete_fields = ['permission']


class UserRoleInline(TabularInline):
    model = UserRole
    extra = 1
    autocomplete_fields = ['user']


@admin.register(Role)
class RoleAdmin(ModelAdmin):
    list_display = ('name', 'is_system', 'permission_count', 'user_count', 'created_at')
    list_filter = ('is_system',)
    search_fields = ('name', 'description')
    inlines = [RolePermissionInline, UserRoleInline]
    fieldsets = (
        ('Əsas Məlumatlar', {
            'fields': ('name', 'description', 'is_system'),
        }),
    )

    @admin.display(description='İcazə sayı')
    def permission_count(self, obj):
        return obj.permissions.count()

    @admin.display(description='İstifadəçi sayı')
    def user_count(self, obj):
        return UserRole.objects.filter(role=obj).count()


@admin.register(Permission)
class PermissionAdmin(ModelAdmin):
    list_display = ('code', 'module', 'description')
    search_fields = ('code', 'module', 'description')
    list_filter = ('module',)
    fieldsets = (
        ('İcazə Məlumatları', {
            'fields': ('code', 'module', 'description'),
        }),
    )


@admin.register(RolePermission)
class RolePermissionAdmin(ModelAdmin):
    list_display = ('role', 'permission')
    list_filter = ('role',)
    autocomplete_fields = ['role', 'permission']


@admin.register(UserRole)
class UserRoleAdmin(ModelAdmin):
    list_display = ('user', 'role', 'created_at')
    list_filter = ('role',)
    autocomplete_fields = ['user', 'role']


@admin.register(AbacPolicy)
class AbacPolicyAdmin(ModelAdmin):
    list_display = ('name', 'resource', 'action', 'created_at')
    search_fields = ('name', 'resource', 'action')
    list_filter = ('resource', 'action')
    fieldsets = (
        ('Əsas Məlumatlar', {
            'fields': ('name', 'description'),
        }),
        ('Siyasət Parametrləri', {
            'fields': ('resource', 'action'),
        }),
        ('Şərt Qaydaları', {
            'fields': ('condition_json',),
            'description': 'JSONLogic formatında şərt qaydalarını daxil edin.',
        }),
    )
