from apps.core.decorators import superuser_required
from django.shortcuts import render
from .models import WorkflowTemplate, WorkflowInstance


@superuser_required
def workflow_dashboard(request):
    """Workflow Engine dashboard — server-side rendering."""
    templates = WorkflowTemplate.objects.all().order_by('-created_at')
    instances = WorkflowInstance.objects.all().order_by('-created_at')[:10]
    context = {
        'templates': templates,
        'instances': instances,
    }
    return render(request, 'workflow_engine/dashboard.html', context)
