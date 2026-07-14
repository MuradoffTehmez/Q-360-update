"""
URL configuration for competencies app.
"""
from django.urls import path
from . import template_views
from . import views_extras

app_name = 'competencies'

# Template-based URLs only - API endpoints are in config/api_urls.py
urlpatterns = [
    path('', template_views.competency_list, name='competency-list'),
    path('my-skills/', template_views.my_skills, name='my-skills'),
    path('gap-analysis/', template_views.skill_gap_analysis, name='gap-analysis'),
    path('manage/', template_views.competency_manage, name='competency-manage'),
    
    # Batch 9
    path('dictionary/', views_extras.competency_dictionary, name='dictionary'),
    path('rating-scales/', views_extras.rating_scales, name='rating-scales'),
    path('behaviors/', views_extras.behavioral_indicators, name='behaviors'),
    
    path('<int:pk>/', template_views.competency_detail, name='competency-detail'),
]
