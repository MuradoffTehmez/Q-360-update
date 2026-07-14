from django.urls import path
from .template_views import workflow_dashboard
from . import views_extras

app_name = 'workflow_engine_ui'

urlpatterns = [
    path('dashboard/', workflow_dashboard, name='dashboard'),

    # Batch 14 - Workflow idarəetmə səhifələri (superuser-only)
    path('workflows/', views_extras.workflows_list, name='workflows'),
    path('designer/', views_extras.workflow_designer, name='designer'),
    path('versions/', views_extras.workflow_versions, name='versions'),
    path('history/', views_extras.workflow_history, name='history'),
    path('logs/', views_extras.workflow_logs, name='logs'),
    path('monitoring/', views_extras.workflow_monitoring, name='monitoring'),
]
