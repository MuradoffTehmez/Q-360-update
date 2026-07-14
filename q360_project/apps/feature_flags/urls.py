from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FeatureFlagViewSet, FeatureFlagRuleViewSet

# Yalnız DRF API router-ləri. UI idarəetmə səhifələri ui_urls.py-dədir
# (superuser-only, /feature-flags/ prefiksində qeydiyyatlıdır).
router = DefaultRouter()
router.register(r'flags', FeatureFlagViewSet)
router.register(r'rules', FeatureFlagRuleViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
