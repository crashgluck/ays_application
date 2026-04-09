"""Estructura RRHH y utilidades para serializarla en el reporte."""

from __future__ import annotations

from typing import Any

RRHH_SECTIONS = [
    {
        "title": "TURNO ALERTA",
        "rows": [
            {"key": "gerente_operaciones", "label": "GERENTE OPERACIONES", "medio_default": "OPS"},
            {"key": "jefe_semana", "label": "JEFE DE SEMANA", "medio_default": "LLAMADO"},
            {"key": "central", "label": "CENTRAL", "medio_default": "CENTRAL"},
            {"key": "alerta_ays", "label": "ALERTA AYS", "medio_default": "LLAMADO"},
        ],
    },
    {
        "title": "PERSONAL DE TURNO COMUNIDAD",
        "rows": [
            {"key": "administracion_1", "label": "ADMINISTRACION 1", "medio_default": "ADM"},
            {"key": "administracion_2", "label": "ADMINISTRACION 2", "medio_default": "ADM"},
            {"key": "administracion_3", "label": "ADMINISTRACION 3", "medio_default": "ADM"},
            {"key": "ggss_encargado_turno", "label": "GGSS ENCARGADO TURNO", "medio_default": "TERRENO"},
            {"key": "ggss_seguridad_1", "label": "GGSS SEGURIDAD 1", "medio_default": ""},
            {"key": "ggss_seguridad_2", "label": "GGSS SEGURIDAD 2", "medio_default": ""},
            {"key": "ggss_seguridad_3", "label": "GGSS SEGURIDAD 3", "medio_default": ""},
            {"key": "jornal_1", "label": "JORNAL 1", "medio_default": "TERRENO"},
            {"key": "jornal_2", "label": "JORNAL 2", "medio_default": "TERRENO"},
            {"key": "jornal_3", "label": "JORNAL 3", "medio_default": "TERRENO"},
            {"key": "drone_1", "label": "DRONE 1", "medio_default": ""},
            {"key": "drone_2", "label": "DRONE 2", "medio_default": ""},
            {"key": "drone_3", "label": "DRONE 3", "medio_default": ""},
            {"key": "brigada_if", "label": "BRIGADA IF", "medio_default": "ADM"},
            {"key": "otro", "label": "OTRO", "medio_default": ""},
            {"key": "externo_sc", "label": "EXTERNO SC", "medio_default": ""},
        ],
    },
    {
        "title": "PERSONAL DE TURNO AYS",
        "rows": [
            {"key": "supervisor", "label": "SUPERVISOR", "medio_default": "OPS"},
            {"key": "administrativo", "label": "ADMINISTRATIVO", "medio_default": "OPS"},
            {"key": "jornal_ays_1", "label": "JORNAL 1", "medio_default": "TERRENO"},
            {"key": "jornal_ays_2", "label": "JORNAL 2", "medio_default": "TERRENO"},
            {"key": "jornal_ays_3", "label": "JORNAL 3", "medio_default": "TERRENO"},
            {"key": "equipo_tecnico_1", "label": "EQUIPO TECNICO 1", "medio_default": "TURNO"},
            {"key": "equipo_tecnico_2", "label": "EQUIPO TECNICO 2", "medio_default": "TURNO"},
            {"key": "equipo_tecnico_3", "label": "EQUIPO TECNICO 3", "medio_default": "TURNO"},
            {"key": "equipo_tecnico_4", "label": "EQUIPO TECNICO 4", "medio_default": "TURNO"},
            {"key": "equipo_tecnico_5", "label": "EQUIPO TECNICO 5", "medio_default": "TURNO"},
            {"key": "taller", "label": "TALLER", "medio_default": "CENTRAL"},
            {"key": "bodega", "label": "BODEGA", "medio_default": "OPS"},
            {"key": "ventas_1", "label": "VENTAS 1", "medio_default": "OPS"},
            {"key": "ventas_2", "label": "VENTAS 2", "medio_default": "OPS"},
            {"key": "hsec", "label": "HSEC", "medio_default": "OPS"},
            {"key": "externo_otro", "label": "EXTERNO / OTRO", "medio_default": ""},
        ],
    },
]


def iter_rrhh_rows():
    for section in RRHH_SECTIONS:
        for row in section["rows"]:
            yield row


def _clean(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def default_rrhh_payload() -> dict[str, dict[str, str]]:
    payload: dict[str, dict[str, str]] = {}
    for row in iter_rrhh_rows():
        payload[row["key"]] = {
            "nombre": "",
            "medio": row.get("medio_default", ""),
            "observacion": "",
        }
    return payload


def normalize_rrhh_payload(payload: Any) -> dict[str, dict[str, str]]:
    normalized = default_rrhh_payload()
    if not isinstance(payload, dict):
        return normalized

    for row in iter_rrhh_rows():
        key = row["key"]
        value = payload.get(key, {})
        if not isinstance(value, dict):
            continue
        normalized[key] = {
            "nombre": _clean(value.get("nombre")),
            "medio": _clean(value.get("medio")) or row.get("medio_default", ""),
            "observacion": _clean(value.get("observacion")),
        }
    return normalized


def build_rrhh_sections(payload: Any) -> list[dict[str, Any]]:
    normalized = normalize_rrhh_payload(payload)
    sections: list[dict[str, Any]] = []
    for section in RRHH_SECTIONS:
        rows: list[dict[str, str]] = []
        for row in section["rows"]:
            key = row["key"]
            value = normalized.get(key, {})
            rows.append(
                {
                    "label": row["label"],
                    "nombre": value.get("nombre", ""),
                    "medio": value.get("medio", row.get("medio_default", "")),
                    "observacion": value.get("observacion", ""),
                }
            )
        sections.append({"title": section["title"], "rows": rows})
    return sections


def get_rrhh_nombre(payload: Any, row_key: str) -> str:
    """Devuelve el nombre de una fila RRHH de forma segura para usar en vistas/reportes."""
    normalized = normalize_rrhh_payload(payload)
    value = normalized.get(row_key, {})
    return _clean(value.get("nombre"))
