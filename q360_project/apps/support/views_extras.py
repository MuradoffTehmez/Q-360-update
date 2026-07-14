from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from .models import SupportTicket, KnowledgeArticle, TicketCategory, SLAPolicy

@login_required
def tickets_list(request):
    """Bütün biletlərin siyahısı."""
    tickets = SupportTicket.objects.all().order_by('-created_at')
    return render(request, 'support/extras/tickets.html', {'title': _('Dəstək Biletləri'), 'tickets': tickets})

@login_required
def knowledge_base(request):
    """Bilik bazası."""
    articles = KnowledgeArticle.objects.all().order_by('-created_at')
    return render(request, 'support/extras/knowledge_base.html', {'title': _('Bilik Bazası (Knowledge Base)'), 'articles': articles})

@login_required
def categories_list(request):
    """Bilet kateqoriyaları."""
    categories = TicketCategory.objects.all()
    return render(request, 'support/extras/categories.html', {'title': _('Kateqoriyalar'), 'categories': categories})

@login_required
def sla_list(request):
    """SLA siyasətləri."""
    slas = SLAPolicy.objects.all()
    return render(request, 'support/extras/sla.html', {'title': _('SLA Siyasətləri'), 'slas': slas})

@login_required
def history_list(request):
    """Dəstək biletlərinin tarixçəsi."""
    return render(request, 'support/extras/history.html', {'title': _('Tarixçə')})
