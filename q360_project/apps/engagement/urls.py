from django.urls import path
from . import views
from . import views_extras

app_name = 'engagement'

urlpatterns = [
    # Dashboard
    path('', views.engagement_dashboard, name='engagement_dashboard'),

    # Pulse Surveys
    path('surveys/', views.pulse_surveys, name='pulse_surveys'),
    path('surveys/<int:survey_id>/', views.survey_detail, name='survey_detail'),

    # Recognition Wall
    path('recognition/', views.recognition_wall, name='recognition_wall'),
    path('recognition/<int:recognition_id>/like/', views.like_recognition, name='like_recognition'),

    # Anonymous Feedback
    path('feedback/', views.anonymous_feedback, name='anonymous_feedback'),

    # Gamification & Leaderboard
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('my-profile/', views.my_profile, name='my_profile'),

    # Batch 26
    path('analytics/', views_extras.analytics_view, name='analytics'),
    path('anonymous-feedback/', views_extras.anonymous_feedback_list, name='anonymous_feedback_list'),
    path('action-plans/', views_extras.action_plans_list, name='action_plans'),
]
