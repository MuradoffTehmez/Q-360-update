from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from .models import SentimentFeedback

@login_required
def reports_list(request):
    """Sentiment hesabatları."""
    # Sadəcə mock məlumat və ya mövcud datalar göstərilə bilər.
    return render(request, 'sentiment_analysis/extras/reports.html', {'title': _('Sentiment Hesabatları (Reports)')})

@login_required
def history_list(request):
    """Sentiment tarixçəsi."""
    history = SentimentFeedback.objects.order_by('-created_at')
    return render(request, 'sentiment_analysis/extras/history.html', {'title': _('Tarixçə (History)'), 'history': history})

@login_required
def trends_list(request):
    """Sentiment trendləri."""
    return render(request, 'sentiment_analysis/extras/trends.html', {'title': _('Trendlər (Trends)')})
