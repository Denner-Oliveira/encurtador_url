from django.db import models
import shortuuid
from datetime import date, timedelta
from typing import Optional

# Create your models here.

class Encurtador(models.Model):
    
    @staticmethod
    def gerar_codigo():
        enc = shortuuid.uuid()[:5]        
        if Encurtador.objects.filter(url_encurtada=enc).exists:
            return enc
        else:
            return None

    @staticmethod
    def gera_data_expiracao(data=None):
        
        if data is None or data > date.today() + timedelta(days=730):
            return date.today() + timedelta(days=365)
        
        # if data > date.today() + timedelta(days=730):
        #     return date.today() + timedelta(days=365)
        
        return data

    url_original = models.URLField()
    url_encurtada = models.CharField(max_length=5,unique=True)
    dt_expiracao = models.DateField(default=gera_data_expiracao())