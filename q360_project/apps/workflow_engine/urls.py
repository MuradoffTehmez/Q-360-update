from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WorkflowTemplateViewSet, WorkflowInstanceViewSet, WorkflowTaskViewSet

# Yalnız DRF API router-ləri. UI idarəetmə səhifələri ui_urls.py-dədir
# (superuser-only, /workflow/ prefiksində qeydiyyatlıdır).
router = DefaultRouter()
router.register(r'templates', WorkflowTemplateViewSet)
router.register(r'instances', WorkflowInstanceViewSet)
router.register(r'tasks', WorkflowTaskViewSet, basename='workflow-tasks')

from .template_views import workflow_dashboard
from . import views_extras

app_name = 'workflow_engine'

urlpatterns = [
    path('api/', include(router.urls)),

    path('dashboard/', workflow_dashboard, name='dashboard'),
    path('workflows/', views_extras.workflows_list, name='workflows'),
    path('designer/', views_extras.workflow_designer, name='designer'),
    path('versions/', views_extras.workflow_versions, name='versions'),
    path('history/', views_extras.workflow_history, name='history'),
    path('logs/', views_extras.workflow_logs, name='logs'),
    path('monitoring/', views_extras.workflow_monitoring, name='monitoring'),
]
