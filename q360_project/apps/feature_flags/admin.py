from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from .models import FeatureFlag, FeatureFlagRule


class FeatureFlagRuleInline(TabularInline):
    model = FeatureFlagRule
    extra = 0
    fields = ('target_users', 'target_departments')


@admin.register(FeatureFlag)
class FeatureFlagAdmin(ModelAdmin):
    list_display = ('name', 'description', 'is_active', 'percentage_rollout', 'rule_count', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    list_editable = ('is_active', 'percentage_rollout')
    inlines = [FeatureFlagRuleInline]
    fieldsets = (
        ('Əsas Məlumatlar', {
            'fields': ('name', 'description'),
        }),
        ('Aktivasiya Ayarları', {
            'fields': ('is_active', 'percentage_rollout'),
            'description': 'Bayrağı aktivləşdirin və istifadəçilərə tətbiq faizini təyin edin.',
        }),
    )

    @admin.display(description='Qayda sayı')
    def rule_count(self, obj):
        return obj.rules.count()


@admin.register(FeatureFlagRule)
class FeatureFlagRuleAdmin(ModelAdmin):
    list_display = ('flag', 'created_at')
    list_filter = ('flag',)
    fieldsets = (
        ('Bayraq Seçimi', {
            'fields': ('flag',),
        }),
        ('Hədəf Qaydaları', {
            'fields': ('target_users', 'target_departments'),
            'description': 'İstifadəçi və departament ID-lərini JSON siyahı formatında daxil edin. Məsələn: [1, 2, 5]',
        }),
    )
