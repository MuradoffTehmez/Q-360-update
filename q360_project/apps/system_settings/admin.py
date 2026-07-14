from django.contrib import admin

from .models import SystemSetting


@admin.register(SystemSetting)
class SystemSettingAdmin(admin.ModelAdmin):
    list_display = ('category', 'key', 'value_type', 'is_sensitive', 'updated_by', 'updated_at')
    list_filter = ('category', 'value_type', 'is_sensitive')
    search_fields = ('category', 'key', 'description')
