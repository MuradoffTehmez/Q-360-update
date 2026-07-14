from django.urls import path
from .template_views import access_control_dashboard
from . import views_extras

app_name = 'access_control_ui'

urlpatterns = [
    path('dashboard/', access_control_dashboard, name='dashboard'),

    # Batch 16 - Access Control idarəetmə səhifələri (superuser-only)
    path('roles/', views_extras.access_roles, name='roles'),
    path('permissions/', views_extras.access_permissions, name='permissions'),
    path('policies/', views_extras.access_policies, name='policies'),
    path('groups/', views_extras.access_groups, name='groups'),
    path('access-requests/', views_extras.access_requests, name='access-requests'),
    path('access-history/', views_extras.access_history, name='access-history'),
]
