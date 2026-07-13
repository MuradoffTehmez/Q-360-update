from functools import wraps
from rest_framework.exceptions import PermissionDenied
from .services import FeatureFlagManager

def feature_required(flag_name):
    """
    Decorator to protect DRF view methods with a feature flag.
    If the flag is inactive, raises PermissionDenied.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(view_instance, request, *args, **kwargs):
            user = request.user if request.user.is_authenticated else None
            if not FeatureFlagManager.is_active(flag_name, user):
                raise PermissionDenied(f"Feature '{flag_name}' is currently disabled.")
            return view_func(view_instance, request, *args, **kwargs)
        return _wrapped_view
    return decorator
