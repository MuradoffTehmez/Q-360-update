from apps.core.decorators import superuser_required
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from .models import WorkflowTemplate, WorkflowVersion, WorkflowHistory, WorkflowLog, WorkflowInstance

@superuser_required
def workflows_list(request):
    """
    Bütün iş axını şablonlarının siyahısı.
    """
    templates = WorkflowTemplate.objects.all()
    
    context = {
        'title': _('İş Axınları (Workflows)'),
        'templates': templates
    }
    return render(request, 'workflow_engine/workflows.html', context)


@superuser_required
def workflow_designer(request):
    """
    Vizual iş axını dizayneri.
    """
    context = {
        'title': _('Vizual Dizayner (Designer)')
    }
    return render(request, 'workflow_engine/designer.html', context)


@superuser_required
def workflow_versions(request):
    """
    İş axını versiyalarının idarə edilməsi.
    """
    versions = WorkflowVersion.objects.select_related('template', 'created_by').all()
    
    context = {
        'title': _('Versiyalar (Versions)'),
        'versions': versions
    }
    return render(request, 'workflow_engine/versions.html', context)


@superuser_required
def workflow_history(request):
    """
    İş axını tarixçəsi.
    """
    history = WorkflowHistory.objects.select_related('instance', 'step', 'actor').all()[:100]
    
    context = {
        'title': _('İş Axını Tarixçəsi'),
        'history': history
    }
    return render(request, 'workflow_engine/history.html', context)


@superuser_required
def workflow_logs(request):
    """
    Sistem loqları.
    """
    logs = WorkflowLog.objects.select_related('instance').all()[:100]
    
    context = {
        'title': _('Sistem Loqları (Logs)'),
        'logs': logs
    }
    return render(request, 'workflow_engine/logs.html', context)


@superuser_required
def workflow_monitoring(request):
    """
    Aktiv instansiyaların monitorinqi.
    """
    instances = WorkflowInstance.objects.select_related('template', 'requester').exclude(status__in=['COMPLETED', 'CANCELLED', 'REJECTED'])
    
    context = {
        'title': _('Monitorinq'),
        'instances': instances
    }
    return render(request, 'workflow_engine/monitoring.html', context)
