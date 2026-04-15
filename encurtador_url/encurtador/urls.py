from django.urls import path
from . import views

urlpatterns = [
    path('shorten-url',views.encurta,name="encurtador"),
    path('search-url',views.consulta_url,name="consultar"),
    path('<str:codigo>',views.redireciona,name="redireciona")
]