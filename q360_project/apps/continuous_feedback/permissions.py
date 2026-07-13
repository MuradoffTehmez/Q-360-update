from rest_framework.permissions import BasePermission
from apps.accounts.rbac import RoleManager

class IsSenderOrAdmin(BasePermission):
    """
    Allow access to feedback sender or administrators.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        user = request.user
        if RoleManager.is_admin(user):
            return True
        
        # Check if obj is PublicRecognition or QuickFeedback
        if hasattr(obj, 'feedback'):
            return obj.feedback.sender == user
        elif hasattr(obj, 'sender'):
            return obj.sender == user
        return False
