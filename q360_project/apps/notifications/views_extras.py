from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from .models import NotificationTemplate, SMSNotification, PushNotification

@login_required
def sms_templates(request):
    """SMS şablonlarının idarə edilməsi."""
    # Sadəlik üçün əsas NotificationTemplate istifadə edirik
    templates = NotificationTemplate.objects.exclude(sms_content='')
    context = {
        'title': _('SMS Şablonları'),
        'templates': templates
    }
    return render(request, 'notifications/sms_templates.html', context)


@login_required
def push_templates(request):
    """Push bildiriş şablonlarının idarə edilməsi."""
    templates = NotificationTemplate.objects.exclude(push_content='')
    context = {
        'title': _('Push Bildiriş Şablonları'),
        'templates': templates
    }
    return render(request, 'notifications/push_templates.html', context)


@login_required
def webhooks_list(request):
    """Sistem webhook-larının idarə edilməsi (Stub/UI)."""
    context = {
        'title': _('Webhook-lar (Tezliklə)')
    }
    return render(request, 'notifications/webhooks.html', context)


@login_required
def notification_queue(request):
    """Gözləyən və göndərilən bildiriş növbəsi."""
    # SMS and Push that are queued
    sms_queued = SMSNotification.objects.filter(status='queued').order_by('scheduled_for')[:20]
    push_queued = PushNotification.objects.filter(status='queued').order_by('scheduled_for')[:20]
    
    context = {
        'title': _('Bildiriş Növbəsi'),
        'sms_queued': sms_queued,
        'push_queued': push_queued
    }
    return render(request, 'notifications/queue.html', context)
