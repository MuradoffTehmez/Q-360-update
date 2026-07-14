"""URL configuration for system settings."""
from django.urls import path

from . import views

app_name = 'system_settings'

urlpatterns = [
    path('', views.settings_home, name='home'),
    path('<slug:category>/', views.settings_category, name='category'),
]
