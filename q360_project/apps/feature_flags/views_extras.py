from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from apps.core.decorators import superuser_required
from .models import FeatureFlag, Environment, RolloutStrategy, Experiment, FeatureFlagLog

@superuser_required
def flag_list(request):
    """
    Xüsusiyyət bayraqlarının siyahısı.
    """
    flags = FeatureFlag.objects.all()
    
    context = {
        'title': _('Xüsusiyyət Bayraqları (Feature Flags)'),
        'flags': flags
    }
    return render(request, 'feature_flags/flags.html', context)


@superuser_required
def flag_environments(request):
    """
    Mühitlər səhifəsi.
    """
    environments = Environment.objects.all()
    
    context = {
        'title': _('Mühitlər (Environments)'),
        'environments': environments
    }
    return render(request, 'feature_flags/environments.html', context)


@superuser_required
def flag_rollouts(request):
    """
    Yayılma strategiyaları.
    """
    rollouts = RolloutStrategy.objects.select_related('flag', 'environment').all()
    
    context = {
        'title': _('Yayılma Strategiyaları (Rollouts)'),
        'rollouts': rollouts
    }
    return render(request, 'feature_flags/rollouts.html', context)


@superuser_required
def flag_experiments(request):
    """
    A/B Eksperimentləri.
    """
    experiments = Experiment.objects.select_related('flag').all()
    
    context = {
        'title': _('A/B Eksperimentlər'),
        'experiments': experiments
    }
    return render(request, 'feature_flags/experiments.html', context)


@superuser_required
def flag_history(request):
    """
    Bayraq dəyişiklik tarixçəsi.
    """
    history = FeatureFlagLog.objects.select_related('flag').all()[:100]
    
    context = {
        'title': _('Bayraq Tarixçəsi (History)'),
        'history': history
    }
    return render(request, 'feature_flags/history.html', context)
