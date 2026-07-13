from django.urls import path
from . import views
from . import api_views
from . import export_views
from . import api

app_name = 'dashboard'

urlpatterns = [
    # Dashboard səhifələri
    path('', views.dashboard_home, name='dashboard_home'),
    path('kpi/', views.kpi_dashboard, name='kpi_dashboard'),
    path('trend/', views.trend_analysis, name='trend_analysis'),
    path('forecast/', views.forecasting_dashboard, name='forecasting_dashboard'),

    # Export endpointləri
    path('export/analytics/excel/', export_views.export_analytics_excel, name='export_analytics_excel'),
    path('export/analytics/pdf/', export_views.export_analytics_pdf, name='export_analytics_pdf'),

    # API endpoints removed to consolidate to /api/v1/dashboard/

    # AI model idarəetmə səhifələri
    path('ai-management/', views.ai_management, name='ai_management'),
    path('train-model/', views.train_model, name='train_model'),
    path('export-model/', views.export_model, name='export_model'),
]
