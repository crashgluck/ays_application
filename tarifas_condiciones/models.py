from django.db import models

# Create your models here.
class Tarifa_PDF(models.Model):
    nombre = models.CharField(max_length=255)
    description = models.TextField(null= True)
    archivo_pdf = models.FileField(upload_to='archivos_pdf/')

class Condiciones_PDF(models.Model):
    nombre = models.CharField(max_length=255)
    description = models.TextField(null= True)
    archivo_pdf = models.FileField(upload_to='archivos_pdf/')