from django.urls import path
from . import template_views
from . import views
from . import views_extras

app_name = 'audit'

# Template-based URLs only - API endpoints would be in config/api_urls.py if needed
urlpatterns = [
    path('security-dashboard/', template_views.security_dashboard, name='security-dashboard'),
    path('log-search/', views.log_search, name='log_search'),
    path('api/block-ip/', template_views.block_ip, name='block-ip'),
    path('api/unblock-ip/', template_views.unblock_ip, name='unblock-ip'),
    
    # Batch 11
    path('events/', views_extras.events_list, name='events'),
    path('login-history/', views_extras.login_history, name='login-history'),
    path('user-history/', views_extras.user_history, name='user-history'),
    path('api/', views_extras.api_logs, name='api'),
    path('security-incidents/', views_extras.security_incidents, name='security-incidents'),
    path('export/', views_extras.export_audit, name='export'),
]
