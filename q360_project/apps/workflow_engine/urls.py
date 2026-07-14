from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WorkflowTemplateViewSet, WorkflowInstanceViewSet, WorkflowTaskViewSet

# Yalnız DRF API router-ləri. UI idarəetmə səhifələri ui_urls.py-dədir
# (superuser-only, /workflow/ prefiksində qeydiyyatlıdır).
router = DefaultRouter()
router.register(r'templates', WorkflowTemplateViewSet)
router.register(r'instances', WorkflowInstanceViewSet)
router.register(r'tasks', WorkflowTaskViewSet, basename='workflow-tasks')

urlpatterns = [
    path('api/', include(router.urls)),
]
