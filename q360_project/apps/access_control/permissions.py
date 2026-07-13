from rest_framework import permissions
from .services import AbacEvaluationService

class IsRbacAuthorized(permissions.BasePermission):
    """
    Checks if user has the required permission code.
    Requires view to define `required_permission`.
    """
    def hasattr_permission(self, view):
        return hasattr(view, 'required_permission')

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
            
        if request.user.is_superuser:
            return True

        if not self.hasattr_permission(view):
            return True # Varsa policy ile yoxla yoxsa aciq burax
        
        required_perm = getattr(view, 'required_permission')
        return request.user.roles.filter(role__permissions__permission__code=required_perm).exists()

class IsAbacAuthorized(permissions.BasePermission):
    """
    Evaluates ABAC policies based on resource and action.
    """
    def has_object_permission(self, request, view, obj):
        # View-da action və resource təyin olunmalıdır
        action = getattr(view, 'abac_action', view.action)
        resource = obj.__class__.__name__
        
        return AbacEvaluationService.evaluate(request.user, resource, action, obj)
