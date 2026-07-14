from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views_extras
from .views import ApprovalChainViewSet, ApprovalDelegationViewSet, PendingApprovalViewSet

router = DefaultRouter()
router.register(r'chains', ApprovalChainViewSet)
router.register(r'delegations', ApprovalDelegationViewSet, basename='approval-delegation')
router.register(r'pending', PendingApprovalViewSet, basename='pending-approval')

urlpatterns = [
    # Batch 15 - Approval UI
    path('rules/', views_extras.approval_rules, name='rules'),
    path('chains/', views_extras.approval_chains, name='chains'),
    path('history/', views_extras.approval_history, name='history'),
    path('queue/', views_extras.approval_queue, name='queue'),
    path('delegations/', views_extras.approval_delegations, name='delegations'),

    path('api/', include(router.urls)),
]
