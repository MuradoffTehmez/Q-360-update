from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views_extras
from .views import WorkflowTemplateViewSet, WorkflowInstanceViewSet, WorkflowTaskViewSet

router = DefaultRouter()
router.register(r'templates', WorkflowTemplateViewSet)
router.register(r'instances', WorkflowInstanceViewSet)
router.register(r'tasks', WorkflowTaskViewSet, basename='workflow-tasks')

urlpatterns = [
    # Batch 14 - Workflow UI
    path('workflows/', views_extras.workflows_list, name='workflows'),
    path('designer/', views_extras.workflow_designer, name='designer'),
    path('versions/', views_extras.workflow_versions, name='versions'),
    path('history/', views_extras.workflow_history, name='history'),
    path('logs/', views_extras.workflow_logs, name='logs'),
    path('monitoring/', views_extras.workflow_monitoring, name='monitoring'),

    path('api/', include(router.urls)),
]
