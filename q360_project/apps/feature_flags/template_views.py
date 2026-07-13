from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import FeatureFlag, FeatureFlagRule


@login_required
def feature_flags_dashboard(request):
    """Feature Flags dashboard — server-side rendering."""
    flags = FeatureFlag.objects.all().order_by('-created_at')
    context = {
        'flags': flags,
    }
    return render(request, 'feature_flags/dashboard.html', context)
