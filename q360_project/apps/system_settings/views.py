"""Views for platform-wide settings pages (admin only)."""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import Http404
from django.shortcuts import render, redirect

from .models import SystemSetting
from .registry import CATEGORIES


def _require_admin(request):
    if not request.user.is_admin():
        messages.error(request, 'Bu səhifəyə giriş icazəniz yoxdur.')
        return redirect('dashboard')
    return None


@login_required
def settings_home(request):
    """Bütün parametr kateqoriyalarının icmalı."""
    denied = _require_admin(request)
    if denied:
        return denied

    counts = {
        row['category']: row['n']
        for row in SystemSetting.objects.values('category').annotate(n=Count('id'))
    }
    categories = [
        {'slug': slug, 'meta': meta, 'count': counts.get(slug, len(meta['defaults'])),
         'is_stub': meta.get('stub', False)}
        for slug, meta in CATEGORIES.items()
    ]
    return render(request, 'system_settings/home.html', {'categories': categories})


@login_required
def settings_category(request, category):
    """Bir kateqoriyanın parametrlərini göstər/yenilə."""
    denied = _require_admin(request)
    if denied:
        return denied

    meta = CATEGORIES.get(category)
    if meta is None:
        raise Http404

    if meta.get('stub'):
        # STUB: MFA/SSO real inteqrasiya spesifikasiyası tələb edir
        return render(request, 'system_settings/stub.html', {
            'category': category, 'meta': meta,
        })

    # Defolt parametrləri lazım olduqda yarat
    existing = {s.key: s for s in SystemSetting.objects.filter(category=category)}
    sensitive_cat = meta.get('sensitive', False)
    for key, default, vtype, desc in meta['defaults']:
        if key not in existing:
            existing[key] = SystemSetting.objects.create(
                category=category, key=key, value=default,
                value_type=vtype, description=desc,
                is_sensitive=sensitive_cat or 'key' in key or 'password' in key,
            )

    settings_list = sorted(existing.values(), key=lambda s: s.key)

    if request.method == 'POST':
        changed = 0
        for setting in settings_list:
            field = f'setting_{setting.id}'
            if setting.value_type == 'bool':
                new_value = 'true' if request.POST.get(field) == 'on' else 'false'
            else:
                if field not in request.POST:
                    continue
                new_value = request.POST.get(field, '').strip()
                if setting.is_sensitive and new_value == '••••••••':
                    continue  # maskalanmış dəyər dəyişdirilməyib
            if new_value != setting.value:
                setting.value = new_value
                setting.updated_by = request.user
                setting.save(update_fields=['value', 'updated_by', 'updated_at'])
                changed += 1
        messages.success(request, f'{changed} parametr yeniləndi.')
        return redirect('system_settings:category', category=category)

    return render(request, 'system_settings/category.html', {
        'category': category, 'meta': meta, 'settings_list': settings_list,
        'categories': CATEGORIES,
    })
