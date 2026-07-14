from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from .models import CriticalRole, RetirementForecast

@login_required
def risk_heatmap(request):
    """
    Kritik rollar üzrə risk xəritəsi (Risk Heatmap).
    """
    critical_roles = CriticalRole.objects.select_related('position', 'current_holder').all()
    
    context = {
        'title': _('Risk Xəritəsi (Heatmap)'),
        'critical_roles': critical_roles
    }
    return render(request, 'workforce_planning/risk_heatmap.html', context)


@login_required
def retirement_forecast(request):
    """
    Təqaüd proqnozları.
    """
    forecasts = RetirementForecast.objects.select_related('user').all()
    
    context = {
        'title': _('Təqaüd Proqnozu'),
        'forecasts': forecasts
    }
    return render(request, 'workforce_planning/retirement_forecast.html', context)
