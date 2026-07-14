from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PolicyViewSet, PolicyVersionViewSet

# Yalnız DRF API router-ləri. UI idarəetmə səhifələri ui_urls.py-dədir
# (superuser-only, /policy-engine/ prefiksində qeydiyyatlıdır).
router = DefaultRouter()
router.register(r'policies', PolicyViewSet)
router.register(r'versions', PolicyVersionViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
