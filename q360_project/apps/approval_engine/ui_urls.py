from django.urls import path
from .template_views import approval_dashboard
from . import views_extras

app_name = 'approval_engine_ui'

urlpatterns = [
    path('dashboard/', approval_dashboard, name='dashboard'),

    # Batch 15 - Approval idarəetmə səhifələri (superuser-only)
    path('rules/', views_extras.approval_rules, name='rules'),
    path('chains/', views_extras.approval_chains, name='chains'),
    path('history/', views_extras.approval_history, name='history'),
    path('queue/', views_extras.approval_queue, name='queue'),
    path('delegations/', views_extras.approval_delegations, name='delegations'),
]
