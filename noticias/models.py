import datetime
from django.db import models

class Noticias(models.Model):
    name = models.CharField(max_length=100)  
    description = models.TextField(default='', blank=True, null=True)
    date = models.DateField(default=datetime.date.today)  # Corrección aquí
    imagen = models.ImageField(upload_to='imagenes/noticias', null=True, blank=True)

    def __str__(self):
        return self.name
