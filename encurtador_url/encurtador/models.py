from django.db import models
import shortuuid

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
    # criador_url = models.CharField(max_length=15,default="Denner")

    def save(self,*args, **kwargs):
        if not self.url_encurtada:
            self.url_encurtada = Encurtador.gerar_codigo()
        super().save(*args, **kwargs)