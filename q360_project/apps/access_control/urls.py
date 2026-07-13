from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoleViewSet, PermissionViewSet, AbacPolicyViewSet

router = DefaultRouter()
router.register(r'roles', RoleViewSet)
router.register(r'permissions', PermissionViewSet)
router.register(r'abac-policies', AbacPolicyViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
