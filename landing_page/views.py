from django.shortcuts import render

from .models import PreguntaFrecuenteAgua, PreguntaFrecuenteEnergia


def inicio(request):
    return render(request, "index.html")


def help(request):
    preguntas_agua = PreguntaFrecuenteAgua.objects.only("pregunta", "respuesta").order_by("id")
    preguntas_energia = PreguntaFrecuenteEnergia.objects.only("pregunta", "respuesta").order_by(
        "id"
    )
    return render(
        request,
        "preguntas_frecuentes/help.html",
        {"preguntas_agua": preguntas_agua, "preguntas_energia": preguntas_energia},
    )


def contacts(request):
    return render(request, "landing/contacts.html")
