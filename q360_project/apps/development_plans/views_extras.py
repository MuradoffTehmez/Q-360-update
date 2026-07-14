from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from .models import DevelopmentGoal, ProgressLog

@login_required
def progress_overview(request):
    """
    Ümumi inkişaf planı irəliləyişi və son fəaliyyətlər.
    """
    recent_logs = ProgressLog.objects.filter(goal__user=request.user).order_by('-created_at')[:20]
    
    context = {
        'title': _('İrəliləyiş İcmalı'),
        'recent_logs': recent_logs
    }
    return render(request, 'development_plans/progress.html', context)


@login_required
def roadmap_view(request):
    """
    Məqsədlərin zaman çizelgesi (roadmap) görünüşü.
    """
    goals = DevelopmentGoal.objects.filter(user=request.user).exclude(status__in=['cancelled', 'rejected']).order_by('target_date')
    
    context = {
        'title': _('İnkişaf Yol Xəritəsi'),
        'goals': goals
    }
    return render(request, 'development_plans/roadmap.html', context)


@login_required
def approvals_queue(request):
    """
    Təsdiq gözləyən məqsədlər (Menecerlər üçün).
    """
    # Assuming the current user is a manager or approver
    pending_goals = DevelopmentGoal.objects.filter(status='pending_approval')
    
    context = {
        'title': _('Təsdiq Növbəsi'),
        'pending_goals': pending_goals
    }
    return render(request, 'development_plans/approvals.html', context)
