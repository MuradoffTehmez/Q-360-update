from rest_framework.renderers import JSONRenderer

class StandardJSONRenderer(JSONRenderer):
    """
    Standartlaşdırılmış JSON formatı:
    {
        "success": true,
        "data": {...},
        "message": "Uğurlu əməliyyat"
    }
    """
    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context.get('response').status_code
        
        # Əgər response success deyilsə (status_code >= 400), xəta handler tərəfindən formatlanır
        if not (200 <= status_code < 300):
            return super().render(data, accepted_media_type, renderer_context)

        # Bəzi hallar üçün artıq standard formatdadırsa
        if isinstance(data, dict) and 'success' in data and ('data' in data or 'error' in data):
            return super().render(data, accepted_media_type, renderer_context)

        response_dict = {
            'success': True,
            'message': 'Uğurlu əməliyyat',
            'data': data
        }

        # Pagination nəticələri olduqda
        if isinstance(data, dict) and 'results' in data and 'count' in data:
            response_dict['data'] = data

        return super().render(response_dict, accepted_media_type, renderer_context)
