from . import views
from django.urls import path

urlpatterns = [
    path('tarifas-condiciones/', views.tarifas_condiciones, name='tarifas_condiciones'), 
    
    
]
