import os

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .rrhh import build_rrhh_sections

DEFAULT_REPORT_RECIPIENTS = [
    "Carlos@forestadezapallar.cl",
    "jaraquemada.julio@gmail.com",
    "maria.jose@forestadezapallar.cl",
    "p.romero@forestadezapallar.cl",
    "seguridad@forestadezapallar.cl",
    "obrasforesta@forestadezapallar.cl",
    "operaciones@forestadezapallar.cl",
]


def get_report_recipients():
    configured = os.getenv("REPORT_EMAIL_RECIPIENTS", "").strip()
    if not configured:
        return DEFAULT_REPORT_RECIPIENTS

    recipients = [email.strip() for email in configured.split(",") if email.strip()]
    return recipients or DEFAULT_REPORT_RECIPIENTS


def send_report_email(reporte):
    html_content = render_to_string(
        "reportes/ver-reportes.html",
        {"reporte": reporte, "rrhh_sections": build_rrhh_sections(reporte.rrhh_registros)},
    )
    email = EmailMultiAlternatives(
        subject="Reporte de Central generado",
        body="Se adjunta el informe en formato HTML.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=get_report_recipients(),
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
