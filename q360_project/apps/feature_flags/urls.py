from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views_extras
from .views import FeatureFlagViewSet, FeatureFlagRuleViewSet

router = DefaultRouter()
router.register(r'flags', FeatureFlagViewSet)
router.register(r'rules', FeatureFlagRuleViewSet)

urlpatterns = [
    # Batch 18 - Feature Flags UI
    path('flags/', views_extras.flag_list, name='flags'),
    path('environments/', views_extras.flag_environments, name='environments'),
    path('rollouts/', views_extras.flag_rollouts, name='rollouts'),
    path('experiments/', views_extras.flag_experiments, name='experiments'),
    path('history/', views_extras.flag_history, name='history'),

    path('api/', include(router.urls)),
]
