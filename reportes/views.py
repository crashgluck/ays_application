from io import BytesIO
import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RRHHMasterStaffForm, ReportForm
from .models import Reporte
from .rrhh import build_rrhh_sections, get_rrhh_nombre
from .rrhh import save_rrhh_personal_vigente
from .services import send_report_email

logger = logging.getLogger(__name__)


def _can_manage_central(user) -> bool:
    return bool(user.is_superuser or user.groups.filter(name="Central").exists())


def _report_contacts(reporte):
    operador = ((reporte.central or "").strip() or get_rrhh_nombre(reporte.rrhh_registros, "central"))
    jefe = (
        (reporte.jefe_semana or "").strip()
        or get_rrhh_nombre(reporte.rrhh_registros, "jefe_semana")
    )
    return operador, jefe


@login_required
def enviar_reporte(request):
    ultimo_reporte = Reporte.objects.order_by("-id").first()

    if request.method == "POST":
        form = ReportForm(request.POST)
        if form.is_valid():
            try:
                reporte = form.save()
            except IntegrityError:
                logger.exception("Error de integridad al guardar reporte")
                form.add_error(
                    None,
                    "No se pudo guardar porque faltan datos obligatorios o hay un valor invalido.",
                )
                messages.error(request, "Corrige los campos marcados antes de guardar.")
            else:
                messages.success(request, f"Reporte #{reporte.id} creado. Revisa y confirma el envio.")
                return redirect("guardar_reporte", reporte_id=reporte.id)
        messages.error(request, "No pudimos guardar el reporte. Revisa los campos marcados.")
    else:
        form = ReportForm(instance=ultimo_reporte)

    return render(
        request,
        "reportes/enviar_reporte.html",
        {"form": form, "has_seed_data": bool(ultimo_reporte)},
    )


@login_required
def guardar_reporte(request, reporte_id):
    reporte = get_object_or_404(Reporte, pk=reporte_id)
    operador_display, jefe_display = _report_contacts(reporte)

    if request.method == "POST":
        if "editar" in request.POST:
            messages.info(
                request,
                (
                    "Regresaste a crear reporte sin eliminar el borrador. "
                    "El ultimo reporte quedara como base para completar los cambios."
                ),
            )
            return redirect("enviar_reporte")

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
                        "operador_display": operador_display,
                        "jefe_display": jefe_display,
                    },
                )

            reporte.confirmado = True
            reporte.save(update_fields=["confirmado"])
            messages.success(request, "Reporte enviado correctamente a los destinatarios configurados.")
            return redirect("report_success")

    return render(
        request,
        "reportes/guardar-reporte.html",
        {
            "reporte": reporte,
            "rrhh_sections": build_rrhh_sections(reporte.rrhh_registros),
            "operador_display": operador_display,
            "jefe_display": jefe_display,
        },
    )


@login_required
def ver_reporte(request, reporte_id):
    reporte = get_object_or_404(Reporte, pk=reporte_id)
    operador_display, jefe_display = _report_contacts(reporte)
    return render(
        request,
        "reportes/ver-reportes.html",
        {
            "reporte": reporte,
            "rrhh_sections": build_rrhh_sections(reporte.rrhh_registros),
            "operador_display": operador_display,
            "jefe_display": jefe_display,
        },
    )


@login_required
def report_success(request):
    return render(request, "reportes/reporte-enviado.html")


@login_required
def report_views(request):
    if not _can_manage_central(request.user):
        return HttpResponseForbidden("No tienes permisos para acceder a Reporte Central.")

    reportes_qs = (
        Reporte.objects.only(
            "id",
            "fecha_hora",
            "central",
            "jefe_semana",
            "rrhh_registros",
            "confirmado",
        )
        .order_by("-id")
    )
    paginator = Paginator(reportes_qs, 20)
    page_obj = paginator.get_page(request.GET.get("page"))
    for reporte in page_obj.object_list:
        reporte.operador_display, reporte.jefe_display = _report_contacts(reporte)
    return render(
        request,
        "reportes/report-views.html",
        {
            "page_obj": page_obj,
            "reportes": page_obj.object_list,
            "can_manage_staff": _can_manage_central(request.user),
        },
    )


@login_required
def administrar_personal(request):
    if not _can_manage_central(request.user):
        return HttpResponseForbidden("No tienes permisos para administrar personal.")

    if request.method == "POST":
        form = RRHHMasterStaffForm(request.POST)
        if form.is_valid():
            try:
                save_rrhh_personal_vigente(form.cleaned_staff_map())
            except Exception:
                logger.exception("Error guardando personal vigente RRHH")
                messages.error(
                    request,
                    "No se pudo guardar el personal vigente. Intenta nuevamente.",
                )
            else:
                messages.success(request, "Personal vigente actualizado correctamente.")
                return redirect("administrar_personal")
        else:
            messages.error(request, "Revisa los campos antes de guardar.")
    else:
        form = RRHHMasterStaffForm()

    return render(request, "reportes/administrar-personal.html", {"form": form})


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
    operador_display, jefe_display = _report_contacts(reporte)
    rrhh_sections = build_rrhh_sections(reporte.rrhh_registros)
    story = [Paragraph(f"<b>Reporte Diario Operativo #{reporte.id}</b>", styles["Title"]), Spacer(1, 4)]

    def v(value):
        return "" if value is None else str(value)

    def section_title(text):
        story.append(Spacer(1, 8))
        story.append(Paragraph(f"<b>{text}</b>", styles["Heading3"]))
        story.append(Spacer(1, 3))

    def make_table(data, col_widths, header_rows=1):
        table = Table(data, colWidths=col_widths, repeatRows=header_rows)
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e5edf7")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9aa8ba")),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f7f9fc")]),
                    ("FONTSIZE", (0, 0), (-1, -1), 8.5),
                    ("LEFTPADDING", (0, 0), (-1, -1), 4),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                    ("TOPPADDING", (0, 0), (-1, -1), 4),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ]
            )
        )
        story.append(table)

    # Resumen
    section_title("Resumen")
    make_table(
        [
            ["Fecha y hora", "Operador Central", "Jefe de Semana"],
            [v(reporte.fecha_hora), v(operador_display), v(jefe_display)],
        ],
        [58 * mm, 58 * mm, 58 * mm],
    )

    # 1) Clima y Riesgos
    section_title("1) Clima y Riesgos")
    make_table(
        [
            ["Item", "Unidad", "Foresta", "Lomas"],
            ["Temperatura", "Celcius", v(reporte.temperatura), v(reporte.lomas_temperatura)],
            ["Viento", "Nudos", v(reporte.viento), v(reporte.lomas_viento)],
            ["Direccion del viento", "Grados", v(reporte.direccion), v(reporte.lomas_direccion)],
            ["Humedad", "%", v(reporte.humedad), v(reporte.lomas_humedad)],
            ["Precipitaciones dia", "mm", v(reporte.precipitaciones_dia), v(reporte.lomas_precipitaciones_dia)],
            ["IGP", "KPI", v(reporte.igp), v(reporte.lomas_igp)],
            ["Nivel de alerta", "KPI", v(reporte.nvl_alerta), v(reporte.lomas_nvl_alerta)],
            ["Factor de seguridad", "KPI", v(reporte.factor_seguridad), "-"],
            ["Nivel riesgos operativos", "KPI", v(reporte.nivel_riesgos_operativos), "-"],
        ],
        [44 * mm, 22 * mm, 54 * mm, 54 * mm],
    )

    # 2) RRHH
    section_title("2) RRHH")
    rrhh_data = [["Cargo", "Nombre", "Medio/Lugar", "Observacion"]]
    for section in rrhh_sections:
        rrhh_data.append([section["title"], "", "", ""])
        for row in section["rows"]:
            rrhh_data.append([v(row.get("label")), v(row.get("nombre")), v(row.get("medio")), v(row.get("observacion"))])
    rrhh_table = Table(rrhh_data, colWidths=[44 * mm, 44 * mm, 38 * mm, 48 * mm], repeatRows=1)
    rrhh_style = TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e5edf7")),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9aa8ba")),
            ("FONTSIZE", (0, 0), (-1, -1), 8.3),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f7f9fc")]),
        ]
    )
    row_index = 1
    for section in rrhh_sections:
        rrhh_style.add("SPAN", (0, row_index), (3, row_index))
        rrhh_style.add("BACKGROUND", (0, row_index), (3, row_index), colors.HexColor("#d4deec"))
        rrhh_style.add("FONTNAME", (0, row_index), (3, row_index), "Helvetica-Bold")
        row_index += 1 + len(section["rows"])
    rrhh_table.setStyle(rrhh_style)
    story.append(rrhh_table)

    # 3) Vehiculos
    section_title("3) Vehiculos Comunidad")
    make_table(
        [
            ["Vehiculo", "Estado", "Odometro (KMS)"],
            ["Movil 13", v(reporte.movil_13_stado), v(reporte.movil_13_odometro)],
            ["Movil 81", v(reporte.movil_11_stado), v(reporte.movil_11_odometro)],
            ["Arriendo", v(reporte.movil_14_stado), v(reporte.movil_14_odometro)],
        ],
        [58 * mm, 58 * mm, 58 * mm],
    )

    # 4) Indicadores
    section_title("4) Indicadores")
    make_table(
        [
            ["Electricos", "Central", "GHR", "Lomas"],
            ["L1", v(reporte.elect_central_l1), v(reporte.elect_ghr_l1), v(reporte.elect_lomas_l1)],
            ["L2", v(reporte.elect_central_l2), v(reporte.elect_ghr_l2), v(reporte.elect_lomas_l2)],
            ["L3", v(reporte.elect_central_l3), v(reporte.elect_ghr_l3), v(reporte.elect_lomas_l3)],
        ],
        [30 * mm, 48 * mm, 48 * mm, 48 * mm],
    )
    story.append(Spacer(1, 4))
    make_table(
        [
            ["Electricos", "SM 3", "SM 1", "Torre Y"],
            ["L1", v(reporte.sm_3_l1), v(reporte.sm_1_l1), v(reporte.torre_y_l1)],
            ["L2", v(reporte.sm_3_l2), v(reporte.sm_1_l2), v(reporte.torre_y_l2)],
            ["L3", v(reporte.sm_3_l3), v(reporte.sm_1_l3), v(reporte.torre_y_l3)],
        ],
        [30 * mm, 48 * mm, 48 * mm, 48 * mm],
    )
    story.append(Spacer(1, 4))
    make_table(
        [
            ["Solar", "3 LED IZQ", "3 LED DER", "Amarillo"],
            ["ON/OFF", v(reporte.solar_central_3led_izq), v(reporte.solar_ghr_3led_der), v(reporte.solar_lomas_led_amarillo)],
            ["Inversores", "INV IZQ", "INV MEDIO", "INV DER"],
            ["Luz roja ON/OFF", v(reporte.inversor_central_izq), v(reporte.inversor_ghr_medio), v(reporte.inversor_lomas_derecho)],
        ],
        [36 * mm, 46 * mm, 46 * mm, 46 * mm],
    )
    story.append(Spacer(1, 4))
    make_table(
        [
            ["Sistema ATLAS/GPS", "Alguna alarma UGPS activa?"],
            [v(reporte.indicar_cual_cctv), v(reporte.alarma_ugps_activa)],
        ],
        [87 * mm, 87 * mm],
    )
    story.append(Spacer(1, 4))
    make_table(
        [
            ["Portones", "Mestiza", "GH", "Cargadero"],
            ["Estado", v(reporte.porton_mestiza), v(reporte.porton_ghr), v(reporte.porton_cargadero)],
            ["Observaciones", v(reporte.porton_mestiza_observaciones), v(reporte.porton_ghr_observaciones), v(reporte.porton_cargadero_observaciones)],
            ["Portones", "Porton I", "Portal Norte", "Sala Mestiza"],
            ["Estado", v(reporte.porton_i), v(reporte.porton_norte), v(reporte.sala_mestiza)],
            ["Observaciones", v(reporte.porton_i_observaciones), v(reporte.porton_norte_observaciones), v(reporte.sala_mestiza_observaciones)],
        ],
        [30 * mm, 48 * mm, 48 * mm, 48 * mm],
    )

    # 5) Operativos
    section_title("5) Operativos")
    make_table(
        [
            ["Item", "Cantidad", "Observacion"],
            ["Vuelos drone dia", v(reporte.vuelos_drone), v(reporte.obs_vuelos_drone)],
            ["Accesos externos turno", v(reporte.accesos_extern_turn), v(reporte.obs_accesos_extern_turn)],
            ["Accesos ventas dia", v(reporte.accesos_ventas_dia), v(reporte.obs_accesos_ventas_dia)],
        ],
        [64 * mm, 30 * mm, 80 * mm],
    )

    # 6) Presiones
    section_title("6) Presiones")
    make_table(
        [
            ["Punto", "Lectura", "Observacion"],
            ["Lomas", v(reporte.presion_lomas), v(reporte.presion_lomas_obs)],
            ["GH", v(reporte.presion_gh), v(reporte.presion_gh_obs)],
            ["SM Ch-2", v(reporte.sm_ch2), v(reporte.sm_ch2_obs)],
            ["SM 3", v(reporte.sm_3), v(reporte.sm_3_obs)],
            ["SM 1", v(reporte.sm_1), v(reporte.sm_1_obs)],
            ["PEAS (Torre Y)", v(reporte.torre_y), v(reporte.torre_y_obs)],
        ],
        [50 * mm, 34 * mm, 90 * mm],
    )

    # 7) Balizas y Sistema CCTV
    section_title("7) Balizas y Sistema CCTV")
    make_table(
        [
            ["Item", "Estado", "Observacion"],
            ["PEAS Aires", v(reporte.peas_aires), v(reporte.obs_peas_aires)],
            ["Cargadero Aires", v(reporte.cargadero_aires), v(reporte.obs_cargadero_aires)],
            ["Planta Solar", v(reporte.planta_solar), "-"],
            ["Sala 1", v(reporte.sala_1), v(reporte.obs_sala_1)],
            ["Sala 2", v(reporte.sala_2), v(reporte.obs_sala_2)],
            ["Sala Club 2", v(reporte.sala_club2), v(reporte.obs_sala_club2)],
            ["Estanques X", v(reporte.estanques_x), v(reporte.obs_estanques_x)],
            ["Mestiza - Belloto", v(reporte.mestiza_belloto), v(reporte.obs_mestiza_belloto)],
            ["Portal GH", v(reporte.elevadora_gh), v(reporte.obs_elevadora_gh)],
            ["Lomas Acceso", v(reporte.lomas_acceso), v(reporte.obs_lomas_acceso)],
            ["Sistema O", v(reporte.sistema_o), v(reporte.obs_sistema_o)],
            ["Pozo CH-1", v(reporte.pozo_ch1), v(reporte.pozo_ch1_observaciones)],
            ["Planta Mirador GH", v(reporte.planta_mirador_gh), v(reporte.planta_mirador_gh_observaciones)],
            ["Pozo P7", v(reporte.pozo_p7), v(reporte.pozo_p7_observaciones)],
            ["Diamante 1", v(reporte.diamante_1), v(reporte.diamante_1_observaciones)],
            ["Diamante 2", v(reporte.diamante_2), v(reporte.diamante_2_observaciones)],
            ["Retamilla dia visible", v(reporte.retamilla_dia_visible), v(reporte.retamilla_dia_visible_observaciones)],
            ["Retamilla noche luz", v(reporte.retamilla_noche_luz), v(reporte.retamilla_noche_luz_observaciones)],
            ["PTAS visible", v(reporte.ptas_visible), v(reporte.ptas_visible_observaciones)],
            ["Lomas", v(reporte.lomas), v(reporte.obs_lomas)],
            ["Otras (verificar)", v(reporte.otras), v(reporte.obs_otras)],
            ["Otras novedades", "-", v(reporte.otras_novedades)],
            ["Observaciones generales", "-", v(reporte.observaciones)],
        ],
        [56 * mm, 36 * mm, 82 * mm],
    )

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
