from apps.core.decorators import superuser_required
from django.shortcuts import render
from .models import Policy, PolicyVersion


@superuser_required
def policy_dashboard(request):
    """Policy Engine dashboard — server-side rendering."""
    policies = Policy.objects.all().order_by('-created_at')
    context = {
        'policies': policies,
    }
    return render(request, 'policy_engine/dashboard.html', context)
