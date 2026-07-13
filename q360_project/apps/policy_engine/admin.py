from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from .models import Policy, PolicyVersion


class PolicyVersionInline(TabularInline):
    model = PolicyVersion
    extra = 1
    fields = ('version_number', 'is_active', 'rule_json')


@admin.register(Policy)
class PolicyAdmin(ModelAdmin):
    list_display = ('name', 'category', 'version_count', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('category',)
    inlines = [PolicyVersionInline]
    fieldsets = (
        ('Əsas Məlumatlar', {
            'fields': ('name', 'category', 'description'),
        }),
    )

    @admin.display(description='Versiya sayı')
    def version_count(self, obj):
        return obj.versions.count()


@admin.register(PolicyVersion)
class PolicyVersionAdmin(ModelAdmin):
    list_display = ('policy', 'version_number', 'is_active', 'created_at')
    list_filter = ('is_active', 'policy')
    list_editable = ('is_active',)
    fieldsets = (
        ('Versiya Məlumatları', {
            'fields': ('policy', 'version_number', 'is_active'),
        }),
        ('Siyasət Qaydaları', {
            'fields': ('rule_json',),
            'description': 'Siyasət qaydalarını JSONLogic formatında daxil edin.',
        }),
    )
