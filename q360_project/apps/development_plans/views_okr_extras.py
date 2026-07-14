from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from .models_okr import KeyResult, ObjectiveUpdate, Initiative, OKRTemplate

@login_required
def key_results_list(request):
    """Bütün Key Result-ların siyahısı."""
    key_results = KeyResult.objects.select_related('objective').all()
    return render(request, 'development_plans/okr_extras/key_results.html', {'title': _('Açar Nəticələr (Key Results)'), 'key_results': key_results})

@login_required
def initiatives_list(request):
    """Təşəbbüslər (Initiatives)."""
    initiatives = Initiative.objects.select_related('owner', 'objective', 'key_result').all()
    return render(request, 'development_plans/okr_extras/initiatives.html', {'title': _('Təşəbbüslər (Initiatives)'), 'initiatives': initiatives})

@login_required
def check_ins_list(request):
    """Objective Updates / Check-ins."""
    check_ins = ObjectiveUpdate.objects.select_related('objective', 'user').order_by('-created_at')
    return render(request, 'development_plans/okr_extras/check_ins.html', {'title': _('Yoxlamalar (Check-ins)'), 'check_ins': check_ins})

@login_required
def templates_list(request):
    """OKR Şablonları."""
    templates = OKRTemplate.objects.all()
    return render(request, 'development_plans/okr_extras/templates.html', {'title': _('OKR Şablonları'), 'templates': templates})
