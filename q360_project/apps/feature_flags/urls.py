from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FeatureFlagViewSet, FeatureFlagRuleViewSet

router = DefaultRouter()
router.register(r'flags', FeatureFlagViewSet)
router.register(r'rules', FeatureFlagRuleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
