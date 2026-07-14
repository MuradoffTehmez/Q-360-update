from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from .models import AuditLog, SecurityIncident, APIRequestLog

@login_required
def events_list(request):
    """
    Sistem hadisələri qeydləri (bütün audit logları).
    """
    events = AuditLog.objects.select_related('user').all()[:100]
    
    context = {
        'title': _('Sistem Hadisələri (Events)'),
        'events': events
    }
    return render(request, 'audit/events.html', context)


@login_required
def login_history(request):
    """
    Sistemə giriş/çıxış tarixçəsi.
    """
    logins = AuditLog.objects.select_related('user').filter(action__in=['login', 'login_failure', 'logout']).order_by('-created_at')[:100]
    
    context = {
        'title': _('Giriş Tarixçəsi'),
        'logins': logins
    }
    return render(request, 'audit/login_history.html', context)


@login_required
def user_history(request):
    """
    İstifadəçi əməliyyatları tarixçəsi.
    """
    history = AuditLog.objects.select_related('user').exclude(action__in=['login', 'login_failure', 'logout'])[:100]
    
    context = {
        'title': _('İstifadəçi Tarixçəsi'),
        'history': history
    }
    return render(request, 'audit/user_history.html', context)


@login_required
def api_logs(request):
    """
    API sorğularının auditi.
    """
    api_requests = APIRequestLog.objects.select_related('user').all()[:100]
    
    context = {
        'title': _('API İzləmə (Logs)'),
        'api_requests': api_requests
    }
    return render(request, 'audit/api_logs.html', context)


@login_required
def security_incidents(request):
    """
    Təhlükəsizlik insidentləri lövhəsi.
    """
    incidents = SecurityIncident.objects.select_related('assigned_to').all()
    
    context = {
        'title': _('Təhlükəsizlik İnsidentləri'),
        'incidents': incidents
    }
    return render(request, 'audit/security_incidents.html', context)


@login_required
def export_audit(request):
    """
    Audit loglarının ixracı bölməsi.
    """
    context = {
        'title': _('Audit İxracı (Export)')
    }
    return render(request, 'audit/export.html', context)
