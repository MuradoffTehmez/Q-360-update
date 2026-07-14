"""URLs for Recruitment module."""
from django.urls import path
from . import views
from . import views_extras

app_name = 'recruitment'

urlpatterns = [
    path('', views.recruitment_dashboard, name='dashboard'),
    path('jobs/', views.job_posting_list, name='job_list'),
    path('jobs/<int:pk>/', views.job_posting_detail, name='job_detail'),
    path('jobs/create/', views.job_posting_create, name='job_create'),
    path('jobs/<int:pk>/edit/', views.job_posting_edit, name='job_edit'),
    path('applications/<int:pk>/', views.application_detail, name='application_detail'),
    path('applications/<int:pk>/status/', views.application_update_status, name='application_update_status'),
    path('applications/<int:pk>/change-status/', views.application_change_status, name='application_change_status'),
    path('applications/<int:pk>/reject/', views.application_reject, name='application_reject'),
    path('applications/<int:pk>/schedule-interview/', views.application_schedule_interview, name='application_schedule_interview'),
    path('applications/<int:pk>/add-note/', views.application_add_note, name='application_add_note'),
    path('interviews/', views.interview_calendar, name='interview_calendar'),
    path('applications/<int:application_id>/interview/', views.interview_create, name='interview_create'),

    # Candidate Pipeline (Kanban)
    path('pipeline/', views.candidate_pipeline, name='candidate_pipeline'),
    path('pipeline/<int:job_id>/', views.candidate_pipeline, name='candidate_pipeline_job'),
    path('applications/<int:application_id>/update-status/', views.update_application_status, name='update_application_status'),

    # AI Screening & Video Interviews
    path('ai-screening/', views.ai_screening, name='ai_screening'),
    path('video-interview-schedule/', views.video_interview_schedule, name='video_interview_schedule'),
    path('candidate-experience/', views.candidate_experience, name='candidate_experience'),

    # Batch 23
    path('candidates/', views_extras.candidates_list, name='candidates'),
    path('offers/', views_extras.offers_list, name='offers'),
    path('talent-pool/', views_extras.talent_pool_list, name='talent_pool'),
    path('referrals/', views_extras.referrals_list, name='referrals'),
    path('interview-feedback/', views_extras.interview_feedback_list, name='interview_feedback'),
]
