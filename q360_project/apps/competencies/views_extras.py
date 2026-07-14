from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from .models import Competency, ProficiencyLevel, BehavioralIndicator

@login_required
def competency_dictionary(request):
    """
    Təşkilatın tam kompetensiya lüğəti.
    """
    competencies = Competency.objects.prefetch_related('behaviors').all()
    
    context = {
        'title': _('Kompetensiya Lüğəti'),
        'competencies': competencies
    }
    return render(request, 'competencies/dictionary.html', context)


@login_required
def rating_scales(request):
    """
    Qiymətləndirmə şkalaları və kompetensiya səviyyələri.
    """
    levels = ProficiencyLevel.objects.all().order_by('score_min')
    
    context = {
        'title': _('Qiymətləndirmə Şkalaları'),
        'levels': levels
    }
    return render(request, 'competencies/rating_scales.html', context)


@login_required
def behavioral_indicators(request):
    """
    Davranış indikatorlarının idarə edilməsi.
    """
    behaviors = BehavioralIndicator.objects.select_related('competency', 'level').all()
    
    context = {
        'title': _('Davranış İndikatorları'),
        'behaviors': behaviors
    }
    return render(request, 'competencies/behaviors.html', context)
