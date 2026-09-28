import json
from django.http import HttpResponse
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
            "Erro": exception.__class__.__name__,
            "Detalhe": str(exception)
        }
        return HttpResponse(
            json.dumps(response_data, indent=4),
            content_type="application/json",
            status=status_code
        )
