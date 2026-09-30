from django.urls import path
from . import views

urlpatterns = [
    path('encurta_url',views.encurta_url,name="encurta_url"),
    path('index',views.index,name="index"),
    path('<str:codigo>',views.redireciona,name="redireciona")    
]