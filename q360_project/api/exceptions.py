from rest_framework.views import exception_handler
from rest_framework.response import Response

def standard_exception_handler(exc, context):
    """
    Standartlaşdırılmış xəta formatı:
    {
        "success": false,
        "error": "...",
        "code": "..."
    }
    """
    response = exception_handler(exc, context)

    if response is not None:
        error_detail = response.data
        if isinstance(error_detail, dict) and 'detail' in error_detail:
            error_message = error_detail['detail']
            error_code = getattr(exc, 'default_code', 'error')
        elif isinstance(error_detail, list):
            error_message = str(error_detail[0])
            error_code = 'validation_error'
        else:
            error_message = str(error_detail)
            error_code = 'validation_error'

        custom_response_data = {
            'success': False,
            'error': error_message,
            'code': getattr(exc, 'default_code', error_code) or 'error'
        }
        
        # Əgər validation error field-level-dirsə, onları da əlavə edək
        if isinstance(error_detail, dict) and 'detail' not in error_detail:
            custom_response_data['error'] = 'Validasiya xətası'
            custom_response_data['code'] = 'validation_error'
            custom_response_data['fields'] = error_detail

        response.data = custom_response_data

    return response
