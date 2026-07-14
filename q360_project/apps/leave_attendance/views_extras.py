from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from .models import LeaveType, Holiday, LeaveBalance, LeaveSettings

@login_required
def leave_types_list(request):
    """Məzuniyyət növləri."""
    types = LeaveType.objects.all()
    return render(request, 'leave_attendance/extras/leave_types.html', {'title': _('Məzuniyyət Növləri (Leave Types)'), 'types': types})

@login_required
def holidays_list(request):
    """Bayramlar."""
    holidays = Holiday.objects.all()
    return render(request, 'leave_attendance/extras/holidays.html', {'title': _('Bayramlar (Holidays)'), 'holidays': holidays})

@login_required
def leave_balances_list(request):
    """İşçilərin məzuniyyət qalıqları."""
    balances = LeaveBalance.objects.select_related('user', 'leave_type').all()
    return render(request, 'leave_attendance/extras/balances.html', {'title': _('Məzuniyyət Qalıqları (Balances)'), 'balances': balances})

@login_required
def carry_over_view(request):
    """Keçid (Carry-over) əməliyyatları."""
    # Nümunə olaraq balances istifadə edirik
    balances = LeaveBalance.objects.select_related('user', 'leave_type').filter(carried_forward_days__gt=0)
    return render(request, 'leave_attendance/extras/carry_over.html', {'title': _('Qalıq Keçidi (Carry Over)'), 'balances': balances})

@login_required
def settings_view(request):
    """Məzuniyyət tənzimləmələri."""
    settings = LeaveSettings.objects.first()
    return render(request, 'leave_attendance/extras/settings.html', {'title': _('Tənzimləmələr (Settings)'), 'settings': settings})
