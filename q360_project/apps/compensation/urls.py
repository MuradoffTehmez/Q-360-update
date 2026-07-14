"""URLs for Compensation module."""
from django.urls import path
from . import views
from . import views_extras

app_name = 'compensation'

urlpatterns = [
    path('', views.compensation_dashboard, name='dashboard'),
    path('salaries/', views.salary_list, name='salary_list'),
    path('salaries/change/', views.salary_change_form, name='salary_change'),
    path('salaries/change/', views.salary_change_form, name='salary-change'),
    path('salaries/change/<int:user_id>/', views.salary_change_form, name='salary_change_user'),
    path('salaries/change/<int:user_id>/', views.salary_change_form, name='salary-change'),
    path('bonuses/', views.bonus_list, name='bonus_list'),
    path('bonuses/create/', views.bonus_create, name='bonus_create'),
    path('history/', views.compensation_history, name='history'),

    # Market Benchmarking & Total Rewards
    path('market-benchmarking/', views.market_benchmarking, name='market_benchmarking'),
    path('total-rewards/', views.total_rewards_statement, name='total_rewards'),

    # Batch 20
    path('pay-grades/', views_extras.pay_grades_list, name='pay_grades'),
    path('salary-bands/', views_extras.salary_bands_list, name='salary_bands'),
    path('currencies/', views_extras.currencies_list, name='currencies'),
    path('cycles/', views_extras.payroll_cycles_list, name='cycles'),
]
