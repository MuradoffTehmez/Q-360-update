from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from .models import ApprovalRule, ApprovalChain, ApprovalLog, ApprovalRequest, ApprovalDelegation

@login_required
def approval_rules(request):
    """
    Təsdiq qaydalarının siyahısı.
    """
    rules = ApprovalRule.objects.select_related('chain').all()
    
    context = {
        'title': _('Təsdiq Qaydaları'),
        'rules': rules
    }
    return render(request, 'approval_engine/rules.html', context)


@login_required
def approval_chains(request):
    """
    Təsdiq zəncirləri səhifəsi.
    """
    chains = ApprovalChain.objects.all()
    
    context = {
        'title': _('Təsdiq Zəncirləri'),
        'chains': chains
    }
    return render(request, 'approval_engine/chains.html', context)


@login_required
def approval_history(request):
    """
    Təsdiq tarixçəsi.
    """
    logs = ApprovalLog.objects.select_related('request', 'actor').all()[:100]
    
    context = {
        'title': _('Tarixçə (History)'),
        'logs': logs
    }
    return render(request, 'approval_engine/history.html', context)


@login_required
def approval_queue(request):
    """
    İstifadəçinin təsdiq gözləyən işləri (queue).
    """
    queue = ApprovalRequest.objects.filter(status='PENDING')
    # Normalda current_node.approver_user = request.user olaraq süzgəcdən keçirilməlidir
    
    context = {
        'title': _('Təsdiq Növbəsi (Queue)'),
        'queue': queue
    }
    return render(request, 'approval_engine/queue.html', context)


@login_required
def approval_delegations(request):
    """
    Təsdiq səlahiyyətlərinin ötürülməsi (delegations).
    """
    delegations = ApprovalDelegation.objects.select_related('delegator', 'delegatee').all()
    
    context = {
        'title': _('Səlahiyyət Ötürülməsi (Delegations)'),
        'delegations': delegations
    }
    return render(request, 'approval_engine/delegations.html', context)
