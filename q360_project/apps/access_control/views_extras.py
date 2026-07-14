from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from .models import Role, Permission, AbacPolicy, UserGroup, AccessRequest, AccessHistory

@login_required
def access_roles(request):
    """
    Rolların siyahısı.
    """
    roles = Role.objects.prefetch_related('permissions__permission').all()
    
    context = {
        'title': _('Rollar'),
        'roles': roles
    }
    return render(request, 'access_control/roles.html', context)


@login_required
def access_permissions(request):
    """
    İcazələrin siyahısı.
    """
    permissions = Permission.objects.all().order_by('module', 'code')
    
    context = {
        'title': _('İcazələr'),
        'permissions': permissions
    }
    return render(request, 'access_control/permissions.html', context)


@login_required
def access_policies(request):
    """
    ABAC siyasətləri.
    """
    policies = AbacPolicy.objects.all()
    
    context = {
        'title': _('ABAC Siyasətləri'),
        'policies': policies
    }
    return render(request, 'access_control/policies.html', context)


@login_required
def access_groups(request):
    """
    İstifadəçi qrupları.
    """
    groups = UserGroup.objects.prefetch_related('roles').all()
    
    context = {
        'title': _('İstifadəçi Qrupları'),
        'groups': groups
    }
    return render(request, 'access_control/groups.html', context)


@login_required
def access_requests(request):
    """
    İcazə tələbləri (queue).
    """
    # Adətən adminlər üçün bütün pending-lər göstərilir
    requests = AccessRequest.objects.filter(status='PENDING').select_related('requester', 'role', 'permission')
    
    context = {
        'title': _('İcazə Tələbləri'),
        'requests': requests
    }
    return render(request, 'access_control/requests.html', context)


@login_required
def access_history(request):
    """
    Giriş tarixçəsi.
    """
    history = AccessHistory.objects.select_related('user').all()[:100]
    
    context = {
        'title': _('Giriş Tarixçəsi'),
        'history': history
    }
    return render(request, 'access_control/history.html', context)
