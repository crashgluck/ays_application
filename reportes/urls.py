from django.urls import path

from . import views

urlpatterns = [
    path('crear-reporte/', views.enviar_reporte, name='enviar_reporte'),
    path('administrar-personal/', views.administrar_personal, name='administrar_personal'),
    path('guardar-reporte/<int:reporte_id>/', views.guardar_reporte, name='guardar_reporte'),
    path('reportes/<int:reporte_id>/', views.ver_reporte, name='ver_reporte'),
    path('reporte-enviado/', views.report_success, name='report_success'),
    path('report-views/', views.report_views, name='report_views'),
    path('<int:reporte_id>/eliminar/', views.eliminar_reporte, name='eliminar_reporte'),
    path('<int:reporte_id>/descargar-pdf/', views.descargar_reporte_pdf, name='descargar_reporte_pdf'),
    
]
