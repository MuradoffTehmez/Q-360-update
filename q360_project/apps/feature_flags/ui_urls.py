from django.urls import path
from .template_views import feature_flags_dashboard
from . import views_extras

app_name = 'feature_flags_ui'

urlpatterns = [
    path('dashboard/', feature_flags_dashboard, name='dashboard'),

    # Batch 18 - Feature Flags idarəetmə səhifələri (superuser-only)
    path('flags/', views_extras.flag_list, name='flags'),
    path('environments/', views_extras.flag_environments, name='environments'),
    path('rollouts/', views_extras.flag_rollouts, name='rollouts'),
    path('experiments/', views_extras.flag_experiments, name='experiments'),
    path('history/', views_extras.flag_history, name='history'),
]
