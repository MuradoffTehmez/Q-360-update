from django.urls import path
from .template_views import policy_dashboard
from . import views_extras

app_name = 'policy_engine_ui'

urlpatterns = [
    path('dashboard/', policy_dashboard, name='dashboard'),

    # Batch 17 - Policy Engine idarəetmə səhifələri (superuser-only)
    path('policies/', views_extras.policy_list, name='policies'),
    path('rules/', views_extras.policy_rules, name='rules'),
    path('simulator/', views_extras.policy_simulator, name='simulator'),
    path('versions/', views_extras.policy_versions, name='versions'),
    path('logs/', views_extras.policy_logs, name='logs'),
]
