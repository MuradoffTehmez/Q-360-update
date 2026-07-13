from django.urls import path
from .template_views import approval_dashboard

app_name = 'approval_engine_ui'

urlpatterns = [
    path('dashboard/', approval_dashboard, name='dashboard'),
]
