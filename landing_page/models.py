from django.db import models

# Create your models here.

class PreguntaFrecuenteAgua(models.Model):
    pregunta = models.CharField(max_length=255, null=False)
    respuesta = models.TextField(blank=False)

    def __str__(self):
        return self.pregunta
    

class PreguntaFrecuenteEnergia(models.Model):
    pregunta = models.CharField(max_length=255, null=False)
    respuesta = models.TextField(blank=False)

    def __str__(self):
        return self.pregunta