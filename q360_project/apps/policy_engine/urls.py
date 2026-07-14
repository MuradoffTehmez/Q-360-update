from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PolicyViewSet, PolicyVersionViewSet

# Yalnız DRF API router-ləri. UI idarəetmə səhifələri ui_urls.py-dədir
# (superuser-only, /policy-engine/ prefiksində qeydiyyatlıdır).
router = DefaultRouter()
router.register(r'policies', PolicyViewSet)
router.register(r'versions', PolicyVersionViewSet)

from .template_views import policy_dashboard
from . import views_extras

app_name = 'policy_engine'

urlpatterns = [
    path('api/', include(router.urls)),

    path('dashboard/', policy_dashboard, name='dashboard'),
    path('policies/', views_extras.policy_list, name='policies'),
    path('rules/', views_extras.policy_rules, name='rules'),
    path('simulator/', views_extras.policy_simulator, name='simulator'),
    path('versions/', views_extras.policy_versions, name='versions'),
    path('logs/', views_extras.policy_logs, name='logs'),
]
