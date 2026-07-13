from django.urls import path
from .template_views import feature_flags_dashboard

app_name = 'feature_flags_ui'

urlpatterns = [
    path('dashboard/', feature_flags_dashboard, name='dashboard'),
]
