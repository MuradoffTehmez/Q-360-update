from django.urls import path
from . import template_views
from . import views

app_name = 'audit'

# Template-based URLs only - API endpoints would be in config/api_urls.py if needed
urlpatterns = [
    path('security-dashboard/', template_views.security_dashboard, name='security-dashboard'),
    path('log-search/', views.log_search, name='log_search'),
    path('api/block-ip/', template_views.block_ip, name='block-ip'),
    path('api/unblock-ip/', template_views.unblock_ip, name='unblock-ip'),
]
