from django.urls import path
from .template_views import workflow_dashboard

app_name = 'workflow_engine_ui'

urlpatterns = [
    path('dashboard/', workflow_dashboard, name='dashboard'),
]
