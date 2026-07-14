from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views_extras
from .views import PolicyViewSet, PolicyVersionViewSet

router = DefaultRouter()
router.register(r'policies', PolicyViewSet)
router.register(r'versions', PolicyVersionViewSet)

urlpatterns = [
    # Batch 17 - Policy Engine UI
    path('policies/', views_extras.policy_list, name='policies'),
    path('rules/', views_extras.policy_rules, name='rules'),
    path('simulator/', views_extras.policy_simulator, name='simulator'),
    path('versions/', views_extras.policy_versions, name='versions'),
    path('logs/', views_extras.policy_logs, name='logs'),

    path('api/', include(router.urls)),
]
