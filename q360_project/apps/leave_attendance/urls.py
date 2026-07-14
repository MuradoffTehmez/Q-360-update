"""URLs for Leave & Attendance module."""
from django.urls import path
from . import views
from . import views_extras

app_name = 'leave_attendance'

urlpatterns = [
    path('', views.leave_dashboard, name='leave_dashboard'),
    path('request/create/', views.leave_request_create, name='leave_request_create'),
    path('requests/', views.leave_request_list, name='leave_request_list'),
    path('attendance/', views.attendance_calendar, name='attendance_calendar'),
    path('team-calendar/', views.team_leave_calendar, name='team_calendar'),

    # Manager approval workflow
    path('approvals/', views.pending_approvals, name='pending_approvals'),
    path('request/<int:pk>/approve/', views.approve_leave_request, name='approve_leave_request'),
    path('request/<int:pk>/reject/', views.reject_leave_request, name='reject_leave_request'),

    # Batch 21
    path('types/', views_extras.leave_types_list, name='leave_types'),
    path('holidays/', views_extras.holidays_list, name='holidays'),
    path('balances/', views_extras.leave_balances_list, name='balances'),
    path('carry-over/', views_extras.carry_over_view, name='carry_over'),
    path('settings/', views_extras.settings_view, name='settings'),
]
