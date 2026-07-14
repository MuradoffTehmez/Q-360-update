"""
URL configuration for departments app.
"""
from django.urls import path
from . import template_views
from . import views_extras

app_name = 'departments'

# Template-based URLs only - API endpoints are in config/api_urls.py
urlpatterns = [
    path('', template_views.DepartmentListView.as_view(), name='department-list'),
    path('structure/', template_views.organization_structure, name='organization-structure'),
    path('chart/', template_views.department_chart, name='department-chart'),
    path('department/<int:pk>/', template_views.DepartmentDetailView.as_view(), name='department-detail'),
    path('department/create/', template_views.DepartmentCreateView.as_view(), name='department-create'),
    path('department/<int:pk>/update/', template_views.DepartmentUpdateView.as_view(), name='department-update'),
    path('department/<int:pk>/delete/', template_views.DepartmentDeleteView.as_view(), name='department-delete'),

    # Batch 5 Extras
    path('positions/', views_extras.position_list, name='positions'),
    path('job-titles/', views_extras.job_title_list, name='job-titles'),
    path('history/', views_extras.department_history, name='history'),
]
