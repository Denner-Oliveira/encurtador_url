from django.urls import path
from . import views

urlpatterns = [
    path('api/v1/encurta_url',views.encurta_url,name="encurta_url"),
    path('',views.index,name="index"),
    path('<str:codigo>',views.redireciona,name="redireciona")    
]