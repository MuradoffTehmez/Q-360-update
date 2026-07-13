def can_view_compensation(request_user, target_user=None):
    """
    Checks if the request_user has permission to view real compensation data
    for the target_user.
    """
    if not request_user or not request_user.is_authenticated:
        return False
        
    if request_user.is_superuser or request_user.role in ['admin', 'hr']:
        return True
        
    if target_user and request_user.id == target_user.id:
        return True
        
    return False

def mask_salary_queryset(queryset, request_user):
    """
    Takes a queryset of SalaryInformation or similar models and masks 
    the financial fields if the user doesn't have permission.
    """
    # Evaluate the queryset to a list so we don't modify the DB
    results = list(queryset)
    for obj in results:
        # Assuming obj has a 'user' attribute
        target_user = getattr(obj, 'user', None)
        if not can_view_compensation(request_user, target_user):
            obj.base_salary = None
            # Also mask other sensitive fields if they exist
            if hasattr(obj, 'amount'):
                obj.amount = None
            if hasattr(obj, 'annual_value'):
                obj.annual_value = None
            if hasattr(obj, 'employee_contribution'):
                obj.employee_contribution = None
    return results

def mask_salary_dict(data_dict, request_user, target_user=None):
    """Masks a dictionary representation of salary."""
    if not can_view_compensation(request_user, target_user):
        sensitive_fields = ['base_salary', 'amount', 'annual_value', 'employee_contribution', 'previous_salary', 'new_salary']
        for field in sensitive_fields:
            if field in data_dict:
                data_dict[field] = None
    return data_dict
