from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ApprovalChainViewSet, ApprovalDelegationViewSet

# Yalnız DRF API router-ləri. UI idarəetmə səhifələri ui_urls.py-dədir
# (superuser-only, /approval/ prefiksində qeydiyyatlıdır).
router = DefaultRouter()
router.register(r'chains', ApprovalChainViewSet)
router.register(r'delegations', ApprovalDelegationViewSet, basename='approval-delegation')

from .template_views import approval_dashboard
from . import views_extras

app_name = 'approval_engine'

urlpatterns = [
    path('api/', include(router.urls)),

    path('dashboard/', approval_dashboard, name='dashboard'),
    path('rules/', views_extras.approval_rules, name='rules'),
    path('chains/', views_extras.approval_chains, name='chains'),
    path('history/', views_extras.approval_history, name='history'),
    path('queue/', views_extras.approval_queue, name='queue'),
    path('delegations/', views_extras.approval_delegations, name='delegations'),
]
