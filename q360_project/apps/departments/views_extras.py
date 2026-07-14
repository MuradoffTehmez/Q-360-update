from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords

from .models import Position, JobTitle, Department, Organization

@login_required
def position_list(request):
    """
    Şöbələrdəki konkret vəzifələrin siyahısı.
    """
    positions = Position.objects.select_related('department', 'organization').all()
    context = {
        'title': _('Vəzifələr'),
        'positions': positions
    }
    return render(request, 'departments/positions.html', context)


@login_required
def job_title_list(request):
    """
    Kataloqdakı standart vəzifə adlarının siyahısı.
    """
    job_titles = JobTitle.objects.all()
    context = {
        'title': _('Vəzifə Kataloqu'),
        'job_titles': job_titles
    }
    return render(request, 'departments/job_titles.html', context)


@login_required
def department_history(request):
    """
    Təşkilat və Şöbələrin dəyişiklik tarixçəsi.
    """
    # Fetch recent history from Organization, Department, Position
    org_history = Organization.history.all()[:10]
    dept_history = Department.history.all()[:10]
    pos_history = Position.history.all()[:10]
    
    # Simple list combining all history
    history_records = []
    
    for h in org_history:
        history_records.append({
            'date': h.history_date,
            'user': h.history_user,
            'type': h.history_type,
            'model': 'Təşkilat',
            'object': h.name
        })
        
    for h in dept_history:
        history_records.append({
            'date': h.history_date,
            'user': h.history_user,
            'type': h.history_type,
            'model': 'Şöbə',
            'object': h.name
        })
        
    for h in pos_history:
        history_records.append({
            'date': h.history_date,
            'user': h.history_user,
            'type': h.history_type,
            'model': 'Vəzifə',
            'object': h.title
        })
        
    # Sort by date descending
    history_records.sort(key=lambda x: x['date'], reverse=True)
    
    context = {
        'title': _('Struktur Tarixçəsi'),
        'history_records': history_records
    }
    return render(request, 'departments/history.html', context)
