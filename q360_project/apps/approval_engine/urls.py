from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ApprovalChainViewSet, ApprovalDelegationViewSet, PendingApprovalViewSet

router = DefaultRouter()
router.register(r'chains', ApprovalChainViewSet)
router.register(r'delegations', ApprovalDelegationViewSet, basename='approval-delegation')
router.register(r'pending', PendingApprovalViewSet, basename='pending-approval')

urlpatterns = [
    path('', include(router.urls)),
]
