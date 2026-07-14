from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from .models import FeedbackTemplate, FeedbackRequest, FeedbackReminder

@login_required
def feedback_templates(request):
    """
    Rəy şablonları səhifəsi.
    """
    templates = FeedbackTemplate.objects.filter(is_active=True)
    
    context = {
        'title': _('Rəy Şablonları'),
        'templates': templates
    }
    return render(request, 'continuous_feedback/templates.html', context)


@login_required
def feedback_requests(request):
    """
    Göndərilən və alınan rəy sorğuları.
    """
    sent_requests = FeedbackRequest.objects.filter(requester=request.user)
    received_requests = FeedbackRequest.objects.filter(recipient=request.user)
    
    context = {
        'title': _('Rəy Sorğuları'),
        'sent_requests': sent_requests,
        'received_requests': received_requests
    }
    return render(request, 'continuous_feedback/requests.html', context)


@login_required
def feedback_reminders(request):
    """
    Rəy xatırlatmaları səhifəsi.
    """
    reminders = FeedbackReminder.objects.filter(user=request.user)
    
    context = {
        'title': _('Xatırlatmalar'),
        'reminders': reminders
    }
    return render(request, 'continuous_feedback/reminders.html', context)
