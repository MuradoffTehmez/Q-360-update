from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Policy, PolicyVersion


@login_required
def policy_dashboard(request):
    """Policy Engine dashboard — server-side rendering."""
    policies = Policy.objects.all().order_by('-created_at')
    context = {
        'policies': policies,
    }
    return render(request, 'policy_engine/dashboard.html', context)
