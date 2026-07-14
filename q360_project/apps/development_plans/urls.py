from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import template_views
from . import views_extras

router = DefaultRouter()

app_name = 'development_plans'

urlpatterns = [
    # Goal views
    path('my-goals/', template_views.my_goals, name='my-goals'),
    path('goals/create/', template_views.GoalCreateView.as_view(), name='goal-create'),
    path('goals/<int:pk>/', template_views.GoalDetailView.as_view(), name='goal-detail'),
    path('goals/<int:pk>/edit/', template_views.GoalUpdateView.as_view(), name='goal-edit'),
    path('goals/<int:pk>/complete/', template_views.goal_complete, name='goal-complete'),
    path('goals/<int:pk>/approve/', template_views.goal_approve, name='goal-approve'),
    path('goals/<int:pk>/toggle-approve/', template_views.goal_approve_toggle, name='goal-approve-toggle'),
    path('goals/<int:goal_pk>/progress/', template_views.add_progress, name='add-progress'),

    # Team and templates
    path('team-goals/', template_views.team_goals, name='team-goals'),
    path('templates/', template_views.goal_templates, name='goal-templates'),

    # Goal Cascade
    path('goal-cascade/', template_views.goal_cascade, name='goal-cascade'),

    # Batch 7 Extras
    path('progress/', views_extras.progress_overview, name='progress-overview'),
    path('roadmap/', views_extras.roadmap_view, name='roadmap-view'),
    path('approvals/', views_extras.approvals_queue, name='approvals-queue'),

    # API
    path('api/', include(router.urls)),
]
