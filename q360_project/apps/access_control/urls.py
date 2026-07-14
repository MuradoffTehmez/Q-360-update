from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views_extras
from .views import RoleViewSet, PermissionViewSet, AbacPolicyViewSet

router = DefaultRouter()
router.register(r'roles', RoleViewSet)
router.register(r'permissions', PermissionViewSet)
router.register(r'abac-policies', AbacPolicyViewSet)

urlpatterns = [
    # Batch 16 - Access Control UI
    path('roles/', views_extras.access_roles, name='roles'),
    path('permissions/', views_extras.access_permissions, name='permissions'),
    path('policies/', views_extras.access_policies, name='policies'),
    path('groups/', views_extras.access_groups, name='groups'),
    path('requests/', views_extras.access_requests, name='requests'),
    path('history/', views_extras.access_history, name='history'),

    path('api/', include(router.urls)),
]
