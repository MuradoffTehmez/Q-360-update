from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    """
    Custom exception handler that standardizes the error response format.
    """
    response = exception_handler(exc, context)
    
    # We let the StandardizedJSONRenderer format the response correctly.
    # We just ensure the response object has the standard attributes needed.
    return response
