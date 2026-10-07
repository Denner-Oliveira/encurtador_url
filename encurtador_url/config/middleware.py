import json
from django.http import JsonResponse
import logging

logger = logging.getLogger(__name__)

class JsonExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):

        status_code = getattr(exception, 'status_code', 500)
        
        logger.error(f"Erro na API: {str(exception)}", exc_info=True)
                
        response_data = {
            "status": getattr(exception,'status_code'),
            "detail": getattr(exception, 'detail', str(exception)),
            "error": getattr(exception, 'default_code', 'INTERNAL_ERROR')            
        }
        return JsonResponse(
            response_data,
            status=status_code
        )
