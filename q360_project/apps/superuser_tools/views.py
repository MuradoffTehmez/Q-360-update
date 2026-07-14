from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.utils.translation import gettext_lazy as _

def superuser_required(function=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_superuser,
        login_url='/accounts/login/'
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

# Files
@superuser_required
def files_dashboard(request):
    return render(request, 'superuser_tools/files_dashboard.html', {'title': _('Fayllar (Files)')})

@superuser_required
def files_uploads(request):
    return render(request, 'superuser_tools/files_uploads.html', {'title': _('Yükləmələr (Uploads)')})

@superuser_required
def files_library(request):
    return render(request, 'superuser_tools/files_library.html', {'title': _('Fayl Kitabxanası (Library)')})

# Data Transfer
@superuser_required
def data_imports(request):
    return render(request, 'superuser_tools/data_imports.html', {'title': _('İmport (İçəri Aktarma)')})

@superuser_required
def data_exports(request):
    return render(request, 'superuser_tools/data_exports.html', {'title': _('Eksport (Xaricə Aktarma)')})

# AI
@superuser_required
def ai_dashboard(request):
    return render(request, 'superuser_tools/ai_dashboard.html', {'title': _('Süni İntellekt (AI)')})

@superuser_required
def ai_prompts(request):
    return render(request, 'superuser_tools/ai_prompts.html', {'title': _('AI Prompts')})

@superuser_required
def ai_models(request):
    return render(request, 'superuser_tools/ai_models.html', {'title': _('AI Modellər')})

@superuser_required
def ai_history(request):
    return render(request, 'superuser_tools/ai_history.html', {'title': _('AI Tarixçə')})

# System
@superuser_required
def system_dashboard(request):
    return render(request, 'superuser_tools/system_dashboard.html', {'title': _('Sistem Paneli')})

@superuser_required
def system_health(request):
    return render(request, 'superuser_tools/system_health.html', {'title': _('Sistem Sağlamlığı (Health)')})

@superuser_required
def system_status(request):
    return render(request, 'superuser_tools/system_status.html', {'title': _('Sistem Statusu')})

@superuser_required
def system_jobs(request):
    return render(request, 'superuser_tools/system_jobs.html', {'title': _('Arxa Plan Tapşırıqları (Jobs)')})

@superuser_required
def system_cache(request):
    return render(request, 'superuser_tools/system_cache.html', {'title': _('Keş İdarəetməsi (Cache)')})

@superuser_required
def system_queues(request):
    return render(request, 'superuser_tools/system_queues.html', {'title': _('Növbələr (Queues)')})

# Admin Extras
@superuser_required
def admin_dashboard(request):
    return render(request, 'superuser_tools/admin_dashboard.html', {'title': _('Admin Paneli')})

@superuser_required
def admin_jobs(request):
    return render(request, 'superuser_tools/admin_jobs.html', {'title': _('Admin Tapşırıqları')})

@superuser_required
def admin_maintenance(request):
    return render(request, 'superuser_tools/admin_maintenance.html', {'title': _('Texniki Xidmət (Maintenance)')})

@superuser_required
def admin_feature_toggles(request):
    return render(request, 'superuser_tools/admin_feature_toggles.html', {'title': _('Xüsusiyyət Dəyişdiriciləri (Feature Toggles)')})
