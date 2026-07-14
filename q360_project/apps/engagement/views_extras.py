from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from .models import AnonymousFeedback, EngagementActionPlan

@login_required
def analytics_view(request):
    """Engagement Analytics."""
    return render(request, 'engagement/extras/analytics.html', {'title': _('Engagement Analitikası')})

@login_required
def anonymous_feedback_list(request):
    """Anonim rəylər."""
    feedbacks = AnonymousFeedback.objects.order_by('-submitted_at')
    return render(request, 'engagement/extras/anonymous_feedback.html', {'title': _('Anonim Rəylər'), 'feedbacks': feedbacks})

@login_required
def action_plans_list(request):
    """Engagement Action Plans."""
    plans = EngagementActionPlan.objects.order_by('start_date')
    return render(request, 'engagement/extras/action_plans.html', {'title': _('Fəaliyyət Planları'), 'plans': plans})
