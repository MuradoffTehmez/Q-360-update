from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PolicyViewSet, PolicyVersionViewSet

router = DefaultRouter()
router.register(r'policies', PolicyViewSet)
router.register(r'versions', PolicyVersionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
