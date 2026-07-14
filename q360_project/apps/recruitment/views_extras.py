from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from .models import Application, Offer, TalentPool, Referral, CandidateExperience

@login_required
def candidates_list(request):
    """Bütün müraciətlər və namizədlər."""
    candidates = Application.objects.select_related('job_posting').order_by('-applied_at')
    return render(request, 'recruitment/extras/candidates.html', {'title': _('Namizədlər (Candidates)'), 'candidates': candidates})

@login_required
def offers_list(request):
    """Təkliflər (Offers)."""
    offers = Offer.objects.select_related('application', 'application__job_posting').order_by('-created_at')
    return render(request, 'recruitment/extras/offers.html', {'title': _('İş Təklifləri (Offers)'), 'offers': offers})

@login_required
def talent_pool_list(request):
    """Talent Pool."""
    pool = TalentPool.objects.all().order_by('-added_at')
    return render(request, 'recruitment/extras/talent_pool.html', {'title': _('Talent Pool'), 'pool': pool})

@login_required
def referrals_list(request):
    """Referrallar (Referrals)."""
    referrals = Referral.objects.select_related('referrer', 'job_posting').order_by('-created_at')
    return render(request, 'recruitment/extras/referrals.html', {'title': _('İstinadlar (Referrals)'), 'referrals': referrals})

@login_required
def interview_feedback_list(request):
    """Müsahibə rəyləri və namizəd təcrübəsi."""
    feedbacks = CandidateExperience.objects.select_related('application', 'application__job_posting').order_by('-feedback_date')
    return render(request, 'recruitment/extras/interview_feedback.html', {'title': _('Müsahibə Rəyləri (Feedback)'), 'feedbacks': feedbacks})
