from django.urls import path
from . import views
from . import views_extras

app_name = 'sentiment_analysis'

urlpatterns = [
    path('dashboard/', views.sentiment_dashboard, name='dashboard'),
    path('feedback/<int:pk>/', views.feedback_detail, name='feedback_detail'),
    path('feedback/<int:pk>/resolve/', views.feedback_resolve, name='feedback_resolve'),

    # Batch 24
    path('reports/', views_extras.reports_list, name='reports'),
    path('history/', views_extras.history_list, name='history'),
    path('trends/', views_extras.trends_list, name='trends'),
]