from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Role, Permission, AbacPolicy


@login_required
def access_control_dashboard(request):
    """Access Control dashboard — server-side rendering."""
    roles = Role.objects.all().order_by('name')
    permissions = Permission.objects.all().order_by('code')
    policies = AbacPolicy.objects.all().order_by('-created_at')
    context = {
        'roles': roles,
        'permissions': permissions,
        'abac_policies': policies,
    }
    return render(request, 'access_control/dashboard.html', context)
