from django.shortcuts import render

from .models import Condiciones_PDF, Tarifa_PDF


def tarifas_condiciones(request):
    condiciones = Condiciones_PDF.objects.only("id", "nombre", "description", "archivo_pdf").order_by(
        "id"
    )
    tarifas = Tarifa_PDF.objects.only("id", "nombre", "description", "archivo_pdf").order_by("id")
    return render(
        request,
        "tarifas_condiciones/inicio.html",
        {"condiciones": condiciones, "tarifas": tarifas},
    )


