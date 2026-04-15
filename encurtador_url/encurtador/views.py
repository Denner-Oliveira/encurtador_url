from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
import json
import shortuuid
from .models import Encurtador
import json

# Create your views here.

def encurta(request):
    
    data = json.loads(request.body.decode('utf-8'))
    link = data["url"]
    link_encurtado = Encurtador.gerar_codigo()    
    if link_encurtado and len(Encurtador.objects.filter(url_original=link)) == 0:
        Encurtador.objects.create(url_original=link,url_encurtada=link_encurtado)
        response = {"url":request.build_absolute_uri(link_encurtado)}
        return HttpResponse(json.dumps(response,indent=4))
    else:
        return HttpResponse(json.dumps({"Erro":"Ja cadastrado"},indent=4))
    
def consulta_url(request):
    url = None
    if request.body: 
        data = json.loads(request.body.decode('utf-8'))
        if data["url"]: 
            url = data["url"]
    if url:
        busca = Encurtador.objects.filter(url_original=url)
        response = {}
        lista = []
        for u in busca:            
            dicionario = {}            
            dicionario["id"],dicionario['url_original'], dicionario['url_encurtada'] = u.id, u.url_original, u.url_encurtada
            lista.append(dicionario)
        response["url"] = lista
    else:       
        busca = list(Encurtador.objects.all())
        response = {}
        lista = []
        for u in busca:            
            dicionario = {}            
            dicionario["id"],dicionario['url_original'], dicionario['url_encurtada'] = u.id, u.url_original, u.url_encurtada
            lista.append(dicionario)                    
        print(lista)
        response["url"] = lista
    return HttpResponse(json.dumps(response,indent=4))

def redireciona(request,codigo):
    url = get_object_or_404(Encurtador,url_encurtada=codigo)
    return redirect(url.url_original)