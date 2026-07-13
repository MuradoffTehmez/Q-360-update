from django.urls import path
from .template_views import access_control_dashboard

app_name = 'access_control_ui'

urlpatterns = [
    path('dashboard/', access_control_dashboard, name='dashboard'),
]
