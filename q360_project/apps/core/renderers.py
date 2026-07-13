from rest_framework.renderers import JSONRenderer

class StandardizedJSONRenderer(JSONRenderer):
    """
    Custom JSON renderer to standardise the API response format.
    Format: {"status": "success"/"error", "data": {...}, "message": "...", "errors": null}
    """
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response_dict = {
            'status': 'success',
            'data': None,
            'message': '',
            'errors': None
        }
        
        # Avoid double wrapping if already formatted
        if isinstance(data, dict) and 'status' in data and 'data' in data:
            return super().render(data, accepted_media_type, renderer_context)
            
        status_code = renderer_context.get('response').status_code if renderer_context else 200
        
        if status_code >= 400:
            response_dict['status'] = 'error'
            response_dict['errors'] = data
            response_dict['message'] = 'An error occurred'
        else:
            response_dict['data'] = data
            response_dict['message'] = 'Success'
            
        return super().render(response_dict, accepted_media_type, renderer_context)
