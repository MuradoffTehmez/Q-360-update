from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ApprovalChain, ApprovalRequest


@login_required
def approval_dashboard(request):
    """Approval Engine dashboard — server-side rendering."""
    chains = ApprovalChain.objects.all().order_by('-created_at')
    requests_list = ApprovalRequest.objects.all().order_by('-created_at')[:10]
    context = {
        'chains': chains,
        'requests_list': requests_list,
    }
    return render(request, 'approval_engine/dashboard.html', context)
