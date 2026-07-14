from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from .models import ReviewCycle, EvaluationTemplate, EvaluationSetting, EvaluationResult

@login_required
def templates_list(request):
    """
    Qiymətləndirmə Şablonlarının siyahısı.
    """
    templates = EvaluationTemplate.objects.all().order_by('-created_at')
    context = {
        'title': _('Qiymətləndirmə Şablonları'),
        'templates': templates
    }
    return render(request, 'evaluations/templates_list.html', context)


@login_required
def review_cycles_list(request):
    """
    Rəy Dövrlərinin siyahısı.
    """
    cycles = ReviewCycle.objects.all().order_by('-start_date')
    context = {
        'title': _('Rəy Dövrləri'),
        'cycles': cycles
    }
    return render(request, 'evaluations/review_cycles.html', context)


@login_required
def evaluation_history(request):
    """
    Keçmiş qiymətləndirmələrin tarixçəsi.
    """
    # User's past evaluations
    results = EvaluationResult.objects.filter(evaluatee=request.user, is_finalized=True).order_by('-calculated_at')
    context = {
        'title': _('Qiymətləndirmə Tarixçəsi'),
        'results': results
    }
    return render(request, 'evaluations/history.html', context)


@login_required
def evaluation_settings(request):
    """
    Qiymətləndirmə parametrlərinin idarə edilməsi.
    """
    setting, created = EvaluationSetting.objects.get_or_create(id=1)
    
    if request.method == 'POST':
        setting.reminder_days = request.POST.get('reminder_days', setting.reminder_days)
        setting.allow_anonymous = request.POST.get('allow_anonymous') == 'on'
        setting.default_self_weight = request.POST.get('default_self_weight', setting.default_self_weight)
        setting.default_supervisor_weight = request.POST.get('default_supervisor_weight', setting.default_supervisor_weight)
        setting.default_peer_weight = request.POST.get('default_peer_weight', setting.default_peer_weight)
        setting.default_subordinate_weight = request.POST.get('default_subordinate_weight', setting.default_subordinate_weight)
        setting.save()
        messages.success(request, _('Parametrlər yadda saxlanıldı.'))
        return redirect('evaluations:settings')
        
    context = {
        'title': _('Qiymətləndirmə Parametrləri'),
        'setting': setting
    }
    return render(request, 'evaluations/settings.html', context)
