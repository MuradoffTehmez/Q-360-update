"""Ortaq view dekoratorları (RBAC / superuser mühafizəsi)."""
from functools import wraps

from django.core.exceptions import PermissionDenied


def superuser_required(view_func=None, *, perm=None):
    """İdarəetmə səhifələrini yalnız superuser (və ya verilmiş `perm`-ə malik
    istifadəçi) üçün açır.

    Digər bütün hallarda (anonim və ya icazəsi olmayan adi istifadəçi)
    ``PermissionDenied`` qaldırılır — bu, HTTP 403 cavabı verir (login-ə
    yönləndirmə DEYİL). Bu davranış superuser-only idarəetmə interfeysləri
    üçün nəzərdə tutulub.

    İstifadə:
        @superuser_required
        def view(request): ...

        @superuser_required(perm='access_control.view_role')
        def view(request): ...
    """

    def decorator(fn):
        @wraps(fn)
        def _wrapped(request, *args, **kwargs):
            user = request.user
            if user.is_authenticated and (user.is_superuser or (perm and user.has_perm(perm))):
                return fn(request, *args, **kwargs)
            raise PermissionDenied
        return _wrapped

    return decorator(view_func) if view_func is not None else decorator
