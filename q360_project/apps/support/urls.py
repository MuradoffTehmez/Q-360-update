from django.urls import path
from . import views
from . import views_extras

app_name = 'support'

urlpatterns = [
    path('', views.support_dashboard, name='dashboard'),
    path('create/', views.ticket_create, name='ticket_create'),
    path('<int:pk>/', views.ticket_detail, name='ticket_detail'),
    path('<int:pk>/close/', views.ticket_close, name='ticket_close'),

    # Batch 27
    path('tickets/', views_extras.tickets_list, name='tickets'),
    path('knowledge-base/', views_extras.knowledge_base, name='knowledge_base'),
    path('categories/', views_extras.categories_list, name='categories'),
    path('sla/', views_extras.sla_list, name='sla'),
    path('history/', views_extras.history_list, name='history'),
]
