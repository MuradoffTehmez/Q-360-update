"""Accounts əlavə səhifələri: sessions, devices, activity, api-tokens, preferences.

Batch 2 — yeni modullar planı üzrə.
"""
import secrets
import hashlib

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.utils import timezone

from apps.audit.models import AuditLog
from apps.notifications.models import PushDevice
from apps.security.session_tracking import UserSessionManager

from .models import APIToken, User, UserPreference


def _get_prefs(user):
    prefs, _created = UserPreference.objects.get_or_create(user=user)
    return prefs


@login_required
def user_sessions(request):
    """Aktiv sessiyaların siyahısı (cari istifadəçi)."""
    sessions = UserSessionManager.get_active_sessions(request.user)
    return render(request, 'accounts/sessions.html', {'sessions': sessions})


@login_required
def user_devices(request):
    """Qeydiyyatlı push cihazları."""
    devices = PushDevice.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'accounts/devices.html', {'devices': devices})


@login_required
def user_activity(request):
    """Cari istifadəçinin fəaliyyət jurnalı."""
    logs = AuditLog.objects.filter(user=request.user).order_by('-created_at')
    paginator = Paginator(logs, 25)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'accounts/activity.html', {'items': page_obj, 'page_obj': page_obj})


@login_required
def api_tokens(request):
    """Şəxsi API tokenlərinin idarə edilməsi."""
    new_token = None
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'create':
            raw = secrets.token_urlsafe(32)
            token = APIToken.objects.create(
                user=request.user,
                name=request.POST.get('name', 'Token')[:100],
                token_prefix=raw[:8],
                token_hash=hashlib.sha256(raw.encode()).hexdigest(),
            )
            new_token = raw
            messages.success(request, f'"{token.name}" tokeni yaradıldı. Tam dəyəri yalnız indi görünür.')
        elif action == 'revoke':
            APIToken.objects.filter(user=request.user, pk=request.POST.get('token_id')).update(is_active=False)
            messages.info(request, 'Token ləğv edildi.')
            return redirect('accounts:api-tokens')
    tokens = APIToken.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'accounts/api_tokens.html', {'tokens': tokens, 'new_token': new_token})


@login_required
def preferences_home(request):
    """İstifadəçi seçimləri — ümumi."""
    prefs = _get_prefs(request.user)
    if request.method == 'POST':
        prefs.language = request.POST.get('language', prefs.language)
        prefs.timezone_name = request.POST.get('timezone_name', prefs.timezone_name)
        prefs.digest_frequency = request.POST.get('digest_frequency', prefs.digest_frequency)
        prefs.save()
        messages.success(request, 'Seçimlər yadda saxlanıldı.')
        return redirect('accounts:preferences')
    return render(request, 'accounts/preferences_home.html', {'prefs': prefs})


@login_required
def preferences_appearance(request):
    """İstifadəçi seçimləri — görünüş."""
    prefs = _get_prefs(request.user)
    if request.method == 'POST':
        prefs.theme = request.POST.get('theme', prefs.theme)
        prefs.density = request.POST.get('density', prefs.density)
        prefs.save()
        messages.success(request, 'Görünüş seçimləri yadda saxlanıldı.')
        return redirect('accounts:preferences-appearance')
    return render(request, 'accounts/preferences_appearance.html', {'prefs': prefs})


@login_required
def preferences_notifications(request):
    """İstifadəçi seçimləri — bildirişlər."""
    prefs = _get_prefs(request.user)
    if request.method == 'POST':
        prefs.notify_email = request.POST.get('notify_email') == 'on'
        prefs.notify_sms = request.POST.get('notify_sms') == 'on'
        prefs.notify_push = request.POST.get('notify_push') == 'on'
        prefs.save()
        messages.success(request, 'Bildiriş seçimləri yadda saxlanıldı.')
        return redirect('accounts:preferences-notifications')
    return render(request, 'accounts/preferences_notifications.html', {'prefs': prefs})
