from django.db import models
import shortuuid
from datetime import date

# Create your models here.

class Encurtador(models.Model):
    
    @staticmethod
    def gerar_codigo():
        enc = shortuuid.uuid()[:5]        
        if Encurtador.objects.filter(url_encurtada=enc).exists:
            return enc
        else:
            return None

    url_original = models.URLField()
    url_encurtada = models.CharField(max_length=5,unique=True)
    dt_expiracao = models.DateField(default=date.today())