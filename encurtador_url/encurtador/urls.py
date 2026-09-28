from django.urls import path
from . import views

urlpatterns = [
    path('encurta_url',views.encurta,name="encurtador"),
    path('busca_url',views.consulta_url,name="consultar"),
    path('<str:codigo>',views.redireciona,name="redireciona")
]