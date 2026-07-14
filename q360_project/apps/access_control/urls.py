from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoleViewSet, PermissionViewSet, AbacPolicyViewSet

# Yalnız DRF API router-ləri. UI idarəetmə səhifələri ui_urls.py-dədir
# (superuser-only, /access-control/ prefiksində qeydiyyatlıdır).
router = DefaultRouter()
router.register(r'roles', RoleViewSet)
router.register(r'permissions', PermissionViewSet)
router.register(r'abac-policies', AbacPolicyViewSet)

from .template_views import access_control_dashboard
from . import views_extras

app_name = 'access_control'

urlpatterns = [
    path('api/', include(router.urls)),
    
    path('dashboard/', access_control_dashboard, name='dashboard'),
    path('roles/', views_extras.access_roles, name='roles'),
    path('permissions/', views_extras.access_permissions, name='permissions'),
    path('policies/', views_extras.access_policies, name='policies'),
    path('groups/', views_extras.access_groups, name='groups'),
    path('access-requests/', views_extras.access_requests, name='access-requests'),
    path('access-history/', views_extras.access_history, name='access-history'),
]
