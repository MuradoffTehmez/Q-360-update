from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from .models import (
    WorkflowTemplate, WorkflowStep, WorkflowCondition,
    WorkflowTransition, WorkflowInstance, WorkflowInstanceStep, WorkflowHistory
)


class WorkflowStepInline(TabularInline):
    model = WorkflowStep
    extra = 1
    fields = ('name', 'step_order', 'step_type', 'description')
    ordering = ('step_order',)


@admin.register(WorkflowTemplate)
class WorkflowTemplateAdmin(ModelAdmin):
    list_display = ('name', 'is_active', 'step_count', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    list_editable = ('is_active',)
    inlines = [WorkflowStepInline]
    fieldsets = (
        ('Əsas Məlumatlar', {
            'fields': ('name', 'description', 'is_active'),
        }),
    )

    @admin.display(description='Addım sayı')
    def step_count(self, obj):
        return obj.steps.count()


@admin.register(WorkflowStep)
class WorkflowStepAdmin(ModelAdmin):
    list_display = ('name', 'template', 'step_order', 'step_type')
    list_filter = ('template', 'step_type')
    search_fields = ('name',)
    ordering = ('template', 'step_order')


@admin.register(WorkflowCondition)
class WorkflowConditionAdmin(ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    fieldsets = (
        ('Əsas Məlumatlar', {
            'fields': ('name',),
        }),
        ('Şərt Qaydaları', {
            'fields': ('rule_json',),
            'description': 'JSON formatında şərt qaydalarını daxil edin.',
        }),
    )


@admin.register(WorkflowTransition)
class WorkflowTransitionAdmin(ModelAdmin):
    list_display = ('source_step', 'destination_step', 'condition')
    list_filter = ('source_step__template',)


class WorkflowInstanceStepInline(TabularInline):
    model = WorkflowInstanceStep
    extra = 0
    readonly_fields = ('step', 'status', 'assigned_to', 'created_at')
    can_delete = False


@admin.register(WorkflowInstance)
class WorkflowInstanceAdmin(ModelAdmin):
    list_display = ('template', 'status', 'requester', 'created_at')
    list_filter = ('status', 'template')
    search_fields = ('template__name', 'requester__email')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [WorkflowInstanceStepInline]


@admin.register(WorkflowInstanceStep)
class WorkflowInstanceStepAdmin(ModelAdmin):
    list_display = ('instance', 'step', 'status', 'assigned_to')
    list_filter = ('status',)


class WorkflowHistoryInline(TabularInline):
    model = WorkflowHistory
    extra = 0
    readonly_fields = ('step', 'actor', 'action', 'comments', 'created_at')
    can_delete = False


@admin.register(WorkflowHistory)
class WorkflowHistoryAdmin(ModelAdmin):
    list_display = ('instance', 'action', 'actor', 'created_at')
    list_filter = ('action',)
    readonly_fields = ('instance', 'step', 'actor', 'action', 'comments', 'created_at')
