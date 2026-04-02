from io import BytesIO
import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ReportForm
from .models import Reporte
from .rrhh import build_rrhh_sections
from .services import send_report_email

logger = logging.getLogger(__name__)


@login_required
def enviar_reporte(request):
    ultimo_reporte = Reporte.objects.order_by("-id").first()

    if request.method == "POST":
        form = ReportForm(request.POST)
        if form.is_valid():
            reporte = form.save()
            messages.success(request, f"Reporte #{reporte.id} creado. Revisa y confirma el envio.")
            return redirect("guardar_reporte", reporte_id=reporte.id)
        messages.error(request, "No pudimos guardar el reporte. Revisa los campos marcados.")
    else:
        form = ReportForm(instance=ultimo_reporte)

    return render(request, "reportes/enviar_reporte.html", {"form": form})


@login_required
def guardar_reporte(request, reporte_id):
    reporte = get_object_or_404(Reporte, pk=reporte_id)

    if request.method == "POST":
        if "volver" in request.POST:
            reporte.delete()
            messages.info(request, "Borrador eliminado. Puedes crear el reporte nuevamente.")
            return redirect("enviar_reporte")

        if "confirmar" in request.POST:
            try:
                send_report_email(reporte)
            except Exception:
                logger.exception("Error enviando correo para reporte %s", reporte.id)
                messages.error(
                    request,
                    "No se pudo enviar el correo automaticamente. Verifica la configuracion de email e intenta nuevamente.",
                )
                return render(
                    request,
                    "reportes/guardar-reporte.html",
                    {
                        "reporte": reporte,
                        "rrhh_sections": build_rrhh_sections(reporte.rrhh_registros),
                    },
                )

            reporte.confirmado = True
            reporte.save(update_fields=["confirmado"])
            messages.success(request, "Reporte enviado correctamente a los destinatarios configurados.")
            return redirect("report_success")

    return render(
        request,
        "reportes/guardar-reporte.html",
        {"reporte": reporte, "rrhh_sections": build_rrhh_sections(reporte.rrhh_registros)},
    )


@login_required
def ver_reporte(request, reporte_id):
    reporte = get_object_or_404(Reporte, pk=reporte_id)
    return render(
        request,
        "reportes/ver-reportes.html",
        {"reporte": reporte, "rrhh_sections": build_rrhh_sections(reporte.rrhh_registros)},
    )


@login_required
def report_success(request):
    return render(request, "reportes/reporte-enviado.html")


@login_required
def report_views(request):
    reportes_qs = (
        Reporte.objects.only("id", "fecha_hora", "central", "jefe_semana", "confirmado")
        .order_by("-id")
    )
    paginator = Paginator(reportes_qs, 20)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(
        request,
        "reportes/report-views.html",
        {"page_obj": page_obj, "reportes": page_obj.object_list},
    )


@login_required
def descargar_reporte_pdf(request, reporte_id):
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib.units import mm
        from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
    except ModuleNotFoundError:
        logger.exception("No se puede generar PDF: falta instalar reportlab.")
        return HttpResponse(
            "No se pudo generar el PDF porque falta la dependencia reportlab.",
            status=503,
            content_type="text/plain",
        )

    reporte = get_object_or_404(Reporte, pk=reporte_id)

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=15 * mm,
        rightMargin=15 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm,
        title=f"Reporte {reporte.id}",
    )

    styles = getSampleStyleSheet()
    story = [
        Paragraph(f"<b>Reporte #{reporte.id}</b>", styles["Title"]),
        Paragraph(f"Fecha/Hora: {reporte.fecha_hora}", styles["Normal"]),
        Spacer(1, 8),
    ]

    def value_or_empty(value):
        return "" if value is None else str(value)

    data = [
        ["Campo", "Valor"],
        ["Temperatura", value_or_empty(reporte.temperatura)],
        ["Viento", value_or_empty(reporte.viento)],
        ["Direccion", value_or_empty(reporte.direccion)],
        ["Humedad", value_or_empty(reporte.humedad)],
        ["Precipitaciones (dia)", value_or_empty(reporte.precipitaciones_dia)],
        ["IGP", value_or_empty(reporte.igp)],
        ["Nivel alerta", value_or_empty(reporte.nvl_alerta)],
        ["Factor seguridad", value_or_empty(reporte.factor_seguridad)],
        ["Nivel riesgos operativos", value_or_empty(reporte.nivel_riesgos_operativos)],
        ["Observaciones", value_or_empty(reporte.observaciones)],
        ["Otras novedades", value_or_empty(reporte.otras_novedades)],
    ]

    table = Table(data, colWidths=[60 * mm, 110 * mm])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.white]),
            ]
        )
    )

    story.append(table)
    doc.build(story)

    pdf = buffer.getvalue()
    buffer.close()

    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="reporte-{reporte.id}.pdf"'
    return response


@login_required
def eliminar_reporte(request, reporte_id):
    reporte = get_object_or_404(Reporte, pk=reporte_id)
    if request.method == "POST":
        reporte.delete()
        messages.success(request, f"Reporte #{reporte_id} eliminado.")
        return redirect("report_views")
    return render(request, "reportes/confirmar_eliminar.html", {"reporte": reporte})
