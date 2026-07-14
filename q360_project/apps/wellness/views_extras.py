from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from .models import Benefit, HealthGoal, VaccinationRecord

@login_required
def benefits_list(request):
    """Müavinətlər və sığortalar."""
    benefits = Benefit.objects.filter(user=request.user).order_by('-start_date')
    return render(request, 'wellness/extras/benefits.html', {'title': _('Müavinətlər və Sığorta'), 'benefits': benefits})

@login_required
def health_goals_list(request):
    """Sağlamlıq Hədəfləri."""
    goals = HealthGoal.objects.filter(user=request.user).order_by('target_date')
    return render(request, 'wellness/extras/health_goals.html', {'title': _('Sağlamlıq Hədəfləri'), 'goals': goals})

@login_required
def vaccinations_list(request):
    """Peyvənd qeydləri."""
    vaccinations = VaccinationRecord.objects.filter(user=request.user).order_by('-administered_date')
    return render(request, 'wellness/extras/vaccinations.html', {'title': _('Peyvənd Qeydləri'), 'vaccinations': vaccinations})
