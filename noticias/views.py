from django.shortcuts import get_object_or_404, render

from .models import Noticias


def noticias(request):
    home_contents = (
        Noticias.objects.only("id", "name", "description", "date", "imagen")
        .order_by("-date", "-id")
    )
    return render(request, "noticias/noticias.html", {"home_contents": home_contents})


def noticia_detalle(request, id):
    noticia = get_object_or_404(Noticias, id=id)
    return render(request, "noticias/noticia_detalle.html", {"noticia": noticia})
