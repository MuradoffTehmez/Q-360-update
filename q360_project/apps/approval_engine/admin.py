from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from .models import ApprovalChain, ApprovalNode, ApprovalRequest, ApprovalDelegation, ApprovalLog


class ApprovalNodeInline(TabularInline):
    model = ApprovalNode
    extra = 1
    fields = ('order', 'node_type', 'approver_user')
    ordering = ('order',)


class ApprovalLogInline(TabularInline):
    model = ApprovalLog
    extra = 0
    readonly_fields = ('node', 'actor', 'action', 'comments', 'created_at')
    can_delete = False


@admin.register(ApprovalChain)
class ApprovalChainAdmin(ModelAdmin):
    list_display = ('name', 'is_active', 'node_count', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    list_editable = ('is_active',)
    inlines = [ApprovalNodeInline]
    fieldsets = (
        ('Əsas Məlumatlar', {
            'fields': ('name', 'description', 'is_active'),
        }),
    )

    @admin.display(description='Qovşaq sayı')
    def node_count(self, obj):
        return obj.nodes.count()


@admin.register(ApprovalNode)
class ApprovalNodeAdmin(ModelAdmin):
    list_display = ('chain', 'order', 'node_type', 'approver_user')
    list_filter = ('chain', 'node_type')
    ordering = ('chain', 'order')


@admin.register(ApprovalRequest)
class ApprovalRequestAdmin(ModelAdmin):
    list_display = ('chain', 'requester', 'status', 'current_node', 'created_at')
    list_filter = ('status', 'chain')
    search_fields = ('chain__name', 'requester__email')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ApprovalLogInline]


@admin.register(ApprovalDelegation)
class ApprovalDelegationAdmin(ModelAdmin):
    list_display = ('delegator', 'delegatee', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active',)
    list_editable = ('is_active',)
    fieldsets = (
        ('Səlahiyyət Məlumatları', {
            'fields': ('delegator', 'delegatee', 'is_active'),
        }),
        ('Tarix Aralığı', {
            'fields': ('start_date', 'end_date'),
        }),
    )


@admin.register(ApprovalLog)
class ApprovalLogAdmin(ModelAdmin):
    list_display = ('request', 'action', 'actor', 'created_at')
    list_filter = ('action',)
    readonly_fields = ('request', 'node', 'actor', 'action', 'comments', 'created_at')
