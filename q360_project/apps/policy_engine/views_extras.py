from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from .models import Policy, PolicyVersion, PolicyRule, PolicyLog

@login_required
def policy_list(request):
    """
    Siyasətlərin siyahısı.
    """
    policies = Policy.objects.all()
    
    context = {
        'title': _('Siyasətlər (Policies)'),
        'policies': policies
    }
    return render(request, 'policy_engine/policies.html', context)


@login_required
def policy_rules(request):
    """
    Siyasət qaydaları.
    """
    rules = PolicyRule.objects.select_related('version__policy').all()
    
    context = {
        'title': _('Siyasət Qaydaları (Rules)'),
        'rules': rules
    }
    return render(request, 'policy_engine/rules.html', context)


@login_required
def policy_simulator(request):
    """
    Simulyator səhifəsi. STUB formadadır.
    """
    context = {
        'title': _('Simulyator')
    }
    return render(request, 'policy_engine/simulator.html', context)


@login_required
def policy_versions(request):
    """
    Siyasət versiyaları.
    """
    versions = PolicyVersion.objects.select_related('policy').all()
    
    context = {
        'title': _('Siyasət Versiyaları'),
        'versions': versions
    }
    return render(request, 'policy_engine/versions.html', context)


@login_required
def policy_logs(request):
    """
    Siyasət əməliyyat tarixçəsi.
    """
    logs = PolicyLog.objects.select_related('policy', 'version').all()[:100]
    
    context = {
        'title': _('Siyasət Jurnalları (Logs)'),
        'logs': logs
    }
    return render(request, 'policy_engine/logs.html', context)
