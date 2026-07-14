"""URLs for P-File module."""
from django.urls import path
from . import views_pfile

app_name = 'pfile'

urlpatterns = [
    path('employees/', views_pfile.employee_list, name='employee_list'),
    path('employees/<int:pk>/', views_pfile.employee_detail, name='employee_detail'),
    path('employees/<int:pk>/edit/', views_pfile.employee_edit, name='employee_edit'),
    path('employees/<int:employee_id>/document/create/', views_pfile.document_create, name='document_create'),
    path('document/<int:pk>/delete/', views_pfile.document_delete, name='document_delete'),
    path('employees/<int:employee_id>/history/create/', views_pfile.history_create, name='history_create'),
    path('history/<int:pk>/delete/', views_pfile.history_delete, name='history_delete'),

    # Batch 19
    path('employees/create/', views_pfile.employee_create, name='employee_create'),
    path('employees/import/', views_pfile.employee_import, name='employee_import'),
    path('documents/', views_pfile.pfile_documents, name='documents'),
    path('contracts/', views_pfile.pfile_contracts, name='contracts'),
    path('assets/', views_pfile.pfile_assets, name='assets'),
    path('emergency-contacts/', views_pfile.pfile_emergency_contacts, name='emergency_contacts'),
]
