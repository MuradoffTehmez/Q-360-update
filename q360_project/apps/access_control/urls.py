from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoleViewSet, PermissionViewSet, AbacPolicyViewSet

# Yalnız DRF API router-ləri. UI idarəetmə səhifələri ui_urls.py-dədir
# (superuser-only, /access-control/ prefiksində qeydiyyatlıdır).
router = DefaultRouter()
router.register(r'roles', RoleViewSet)
router.register(r'permissions', PermissionViewSet)
router.register(r'abac-policies', AbacPolicyViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
