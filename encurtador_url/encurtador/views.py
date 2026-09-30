from django.shortcuts import render,get_object_or_404,redirect
from django.http import request, JsonResponse, Http404
from .exceptions import RequisicaoIncompletaEncurtaException, RequisicaoIncompletaEncurtaURLException, DuplicidadeURLCadastradaException, FalhaNoServidorException, URLExpiradaException, URLNaoEncontradaException
import json
from .models import Encurtador
import json
from datetime import date
from django.views.decorators.http import require_http_methods, require_POST, require_GET

# Create your views here.

@require_POST
def encurta_url(request:request):

    if len(request.body.decode('utf-8')) == 0:
        raise RequisicaoIncompletaEncurtaException()

    try:
        data:dict = json.loads(request.body.decode('utf-8'))
        
        if data["url"] is None:
            raise RequisicaoIncompletaEncurtaURLException()
        
        link = data["url"]
        link_encurtado = Encurtador.gerar_codigo()
    except ValueError as error:
        raise FalhaNoServidorException()
    
    if link_encurtado:
        Encurtador.objects.create(url_original=link,url_encurtada=link_encurtado,dt_expiracao=Encurtador.gera_data_expiracao())
        response = {"url":request.build_absolute_uri(link_encurtado)}
        return JsonResponse(response,json_dumps_params={'indent':4})

@require_GET
def index(request:request):
    return render(request,template_name='encurtador/index.html')
    
@require_GET
def redireciona(request:request,codigo):

    try:
        url = get_object_or_404(Encurtador,url_encurtada=codigo)    
    except Http404 as error:
        raise URLNaoEncontradaException()        
    
    if url.dt_expiracao < date.today():
        raise URLExpiradaException()
    return redirect(url.url_original)

def erro_404(request, exception):
    return JsonResponse({
        "status": 404,        
        "detail": "URL nao encontrada",
        "error": "NOT_FOUND",
    }, status=404)

