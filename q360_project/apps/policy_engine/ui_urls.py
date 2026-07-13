from django.urls import path
from .template_views import policy_dashboard

app_name = 'policy_engine_ui'

urlpatterns = [
    path('dashboard/', policy_dashboard, name='dashboard'),
]
