from . import views
from django.urls import path

urlpatterns = [
    path('', views.inicio, name='inicio'), 
    path('help/', views.help, name='help'),
    path('contactos/', views.contacts, name='contacts'),
]
