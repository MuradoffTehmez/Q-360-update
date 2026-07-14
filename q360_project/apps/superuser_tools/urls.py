from django.urls import path
from . import views

app_name = 'superuser_tools'

urlpatterns = [
    # Files
    path('files/', views.files_dashboard, name='files_dashboard'),
    path('files/uploads/', views.files_uploads, name='files_uploads'),
    path('files/library/', views.files_library, name='files_library'),

    # Data Transfer
    path('imports/', views.data_imports, name='imports'),
    path('exports/', views.data_exports, name='exports'),

    # AI
    path('ai/', views.ai_dashboard, name='ai_dashboard'),
    path('ai/prompts/', views.ai_prompts, name='ai_prompts'),
    path('ai/models/', views.ai_models, name='ai_models'),
    path('ai/history/', views.ai_history, name='ai_history'),

    # System
    path('system/', views.system_dashboard, name='system_dashboard'),
    path('system/health/', views.system_health, name='system_health'),
    path('system/status/', views.system_status, name='system_status'),
    path('system/jobs/', views.system_jobs, name='system_jobs'),
    path('system/cache/', views.system_cache, name='system_cache'),
    path('system/queues/', views.system_queues, name='system_queues'),

    # Admin Extras
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/jobs/', views.admin_jobs, name='admin_jobs'),
    path('admin-panel/maintenance/', views.admin_maintenance, name='admin_maintenance'),
    path('admin-panel/feature-toggles/', views.admin_feature_toggles, name='admin_feature_toggles'),
]
