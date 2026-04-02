from django.urls import path

from . import views

urlpatterns = [
    path('noticias/', views.noticias, name='noticias'),
    path('noticia/<int:id>/', views.noticia_detalle, name='noticia_detalle'),
]
