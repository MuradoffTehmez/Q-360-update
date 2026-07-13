from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReviewSessionViewSet

app_name = 'performance_reviews'

router = DefaultRouter()
router.register(r'sessions', ReviewSessionViewSet, basename='session')

urlpatterns = [
    # path('api/', include(router.urls)), # Removed to consolidate to /api/v1/
]
