from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WorkflowTemplateViewSet, WorkflowInstanceViewSet, WorkflowTaskViewSet

router = DefaultRouter()
router.register(r'templates', WorkflowTemplateViewSet)
router.register(r'instances', WorkflowInstanceViewSet)
router.register(r'tasks', WorkflowTaskViewSet, basename='workflow-tasks')

urlpatterns = [
    path('', include(router.urls)),
]
