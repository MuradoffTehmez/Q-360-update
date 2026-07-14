from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FeatureFlagViewSet, FeatureFlagRuleViewSet

# Yalnız DRF API router-ləri. UI idarəetmə səhifələri ui_urls.py-dədir
# (superuser-only, /feature-flags/ prefiksində qeydiyyatlıdır).
router = DefaultRouter()
router.register(r'flags', FeatureFlagViewSet)
router.register(r'rules', FeatureFlagRuleViewSet)

from .template_views import feature_flags_dashboard
from . import views_extras

app_name = 'feature_flags'

urlpatterns = [
    path('api/', include(router.urls)),

    path('dashboard/', feature_flags_dashboard, name='dashboard'),
    path('flags/', views_extras.flag_list, name='flags'),
    path('environments/', views_extras.flag_environments, name='environments'),
    path('rollouts/', views_extras.flag_rollouts, name='rollouts'),
    path('experiments/', views_extras.flag_experiments, name='experiments'),
    path('history/', views_extras.flag_history, name='history'),
]
