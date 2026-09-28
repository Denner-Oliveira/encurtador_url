from django.shortcuts import render,get_object_or_404,redirect
from django.http import request, JsonResponse
from .exceptions import RequisicaoIncompletaEncurtaException, RequisicaoIncompletaEncurtaURLException, DuplicidadeURLCadastradaException, FalhaNoServidorException, URLExpiradaException, URLNaoEncontradaException
import json
from .models import Encurtador
import json
from datetime import date

# Create your views here.

def encurta(request:request):

    try:
        if len(request.body.decode('utf-8')) == 0:
            raise RequisicaoIncompletaEncurtaException()

        data:dict = json.loads(request.body.decode('utf-8'))
        
        if data["url"] is None:
            raise RequisicaoIncompletaEncurtaURLException()
        
        link = data["url"]
        link_encurtado = Encurtador.gerar_codigo()
        
        if link_encurtado and len(Encurtador.objects.filter(url_original=link)) == 0:
            dt_expiracao = data.get("dt_expiracao") or Encurtador.expiracao_padrao()        
            Encurtador.objects.create(url_original=link,url_encurtada=link_encurtado,dt_expiracao=dt_expiracao)
            response = {"url":request.build_absolute_uri(link_encurtado)}
            return JsonResponse(response,json_dumps_params={'indent':4})
        else:
            raise DuplicidadeURLCadastradaException()
    except Exception as error:
        raise FalhaNoServidorException()

def __iterador_busca(busca):
    lista = []
    
    for u in busca:  
        dicionario = {}                  
        dicionario['url_original'], dicionario['url_encurtada'],dicionario["dt_expiracao"] = u.url_original, u.url_encurtada, u.dt_expiracao.strftime("%d/%m/%Y")
        lista.append(dicionario)
    return lista

def consulta_url(request:request):

    try:
        url = None
        response = {}

        if not len(request.body.decode('utf-8')) == 0:
            data = json.loads(request.body.decode('utf-8'))
            if data["url"]: 
                url = data["url"]

        if url:
            busca = Encurtador.objects.filter(url_original=url)
            if busca is None:
                raise URLNaoEncontradaException()
            response["response"] = __iterador_busca(busca)
        else:       
            busca = list(Encurtador.objects.all())              
            if busca is None:
                raise URLNaoEncontradaException()    
            response["response"] = __iterador_busca(busca)
        return JsonResponse(response,json_dumps_params={'indent':4})
    except Exception as error:
        raise FalhaNoServidorException()

def redireciona(request:request,codigo):

    try:
        url = get_object_or_404(Encurtador,url_encurtada=codigo)    
        if url.dt_expiracao > date.today():
            raise URLExpiradaException()
        return redirect(url.url_original)
    except Exception as error:
        raise FalhaNoServidorException()