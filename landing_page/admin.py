from django.contrib import admin
from .models import PreguntaFrecuenteAgua, PreguntaFrecuenteEnergia

# Register your models here.
admin.site.register(PreguntaFrecuenteAgua)
admin.site.register(PreguntaFrecuenteEnergia)