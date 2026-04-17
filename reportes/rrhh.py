"""Estructura RRHH y utilidades para serializarla en el reporte."""

from __future__ import annotations

import json
from pathlib import Path
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

RRHH_STAFF_FILE = Path(__file__).with_name("rrhh_personal_vigente.json")

# Fallback usado solo si el JSON no existe o tiene formato invalido.
# La llave de cada item corresponde a row["key"] de RRHH_SECTIONS.
DEFAULT_RRHH_PERSONAL_VIGENTE = {
    "gerente_operaciones": "NOMBRE GERENTE",
    "jefe_semana": "NOMBRE JEFE SEMANA",
    "central": "NOMBRE CENTRAL",
    "alerta_ays": "NOMBRE ALERTA AYS",
    "administracion_1": "NOMBRE ADMIN 1",
    "administracion_2": "NOMBRE ADMIN 2",
    "administracion_3": "NOMBRE ADMIN 3",
    "ggss_encargado_turno": "NOMBRE GGSS ENCARGADO",
    "ggss_seguridad_1": "NOMBRE GGSS 1",
    "ggss_seguridad_2": "NOMBRE GGSS 2",
    "ggss_seguridad_3": "NOMBRE GGSS 3",
    "jornal_1": "NOMBRE JORNAL 1",
    "jornal_2": "NOMBRE JORNAL 2",
    "jornal_3": "NOMBRE JORNAL 3",
    "drone_1": "NOMBRE DRONE 1",
    "drone_2": "NOMBRE DRONE 2",
    "drone_3": "NOMBRE DRONE 3",
    "brigada_if": "NOMBRE BRIGADA IF",
    "otro": "",
    "externo_sc": "",
    "supervisor": "NOMBRE SUPERVISOR",
    "administrativo": "NOMBRE ADMINISTRATIVO",
    "jornal_ays_1": "NOMBRE JORNAL AYS 1",
    "jornal_ays_2": "NOMBRE JORNAL AYS 2",
    "jornal_ays_3": "NOMBRE JORNAL AYS 3",
    "equipo_tecnico_1": "NOMBRE TECNICO 1",
    "equipo_tecnico_2": "NOMBRE TECNICO 2",
    "equipo_tecnico_3": "NOMBRE TECNICO 3",
    "equipo_tecnico_4": "NOMBRE TECNICO 4",
    "equipo_tecnico_5": "NOMBRE TECNICO 5",
    "taller": "NOMBRE TALLER",
    "bodega": "NOMBRE BODEGA",
    "ventas_1": "NOMBRE VENTAS 1",
    "ventas_2": "NOMBRE VENTAS 2",
    "hsec": "NOMBRE HSEC",
    "externo_otro": "",
}


def iter_rrhh_rows():
    for section in RRHH_SECTIONS:
        for row in section["rows"]:
            yield row


def _clean(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _valid_rrhh_keys() -> set[str]:
    return {row["key"] for row in iter_rrhh_rows()}


def _empty_staff_map() -> dict[str, str]:
    return {key: "" for key in _valid_rrhh_keys()}


def _load_rrhh_personal_vigente_from_json() -> dict[str, str]:
    if not RRHH_STAFF_FILE.exists():
        source = DEFAULT_RRHH_PERSONAL_VIGENTE
    else:
        try:
            with RRHH_STAFF_FILE.open("r", encoding="utf-8") as fh:
                raw = json.load(fh)
            source = raw if isinstance(raw, dict) else DEFAULT_RRHH_PERSONAL_VIGENTE
        except (OSError, json.JSONDecodeError):
            source = DEFAULT_RRHH_PERSONAL_VIGENTE

    cleaned = _empty_staff_map()
    for key in cleaned:
        cleaned[key] = _clean(source.get(key, ""))
    return cleaned


def _load_rrhh_personal_vigente_from_db() -> dict[str, str] | None:
    try:
        from django.db.utils import OperationalError, ProgrammingError
        from .models import RRHHPersonalVigente
    except Exception:
        return None

    try:
        rows = RRHHPersonalVigente.objects.all().only("row_key", "nombre_vigente")
    except (OperationalError, ProgrammingError):
        return None

    valid_keys = _valid_rrhh_keys()
    data = _empty_staff_map()
    found_any = False
    for row in rows:
        if row.row_key not in valid_keys:
            continue
        data[row.row_key] = _clean(row.nombre_vigente)
        found_any = True
    return data if found_any else {}


def load_rrhh_personal_vigente() -> dict[str, str]:
    """Lee la lista maestra de personal vigente.

    Prioridad:
    1) BD (RRHHPersonalVigente)
    2) JSON local (fallback)

    Formato esperado para fallback JSON:
    {
      "row_key": "NOMBRE PERSONA",
      ...
    }
    """
    db_data = _load_rrhh_personal_vigente_from_db()
    if db_data is None or not any(db_data.values()):
        return _load_rrhh_personal_vigente_from_json()
    return db_data


def save_rrhh_personal_vigente(staff_map: dict[str, str]) -> None:
    """Guarda la lista maestra vigente en BD de forma atomica y validada."""
    from django.db import transaction
    from .models import RRHHPersonalVigente

    valid_keys = _valid_rrhh_keys()
    normalized = {key: _clean(staff_map.get(key, "")) for key in valid_keys}

    with transaction.atomic():
        existing = {
            item.row_key: item
            for item in RRHHPersonalVigente.objects.filter(row_key__in=valid_keys)
        }

        create_batch = []
        update_batch = []
        for key in valid_keys:
            value = normalized[key]
            current = existing.get(key)
            if current is None:
                create_batch.append(RRHHPersonalVigente(row_key=key, nombre_vigente=value))
                continue
            if current.nombre_vigente != value:
                current.nombre_vigente = value
                update_batch.append(current)

        if create_batch:
            RRHHPersonalVigente.objects.bulk_create(create_batch)
        if update_batch:
            RRHHPersonalVigente.objects.bulk_update(update_batch, ["nombre_vigente"])

        RRHHPersonalVigente.objects.exclude(row_key__in=valid_keys).delete()


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


def build_rrhh_initial_payload(payload: Any) -> dict[str, dict[str, str]]:
    """Prioridad de carga RRHH:

    1) Lista maestra vigente para nombres
    2) Ultimo reporte para campos reutilizables (medio/observacion)
    3) Valores por defecto de seccion
    """
    historical = normalize_rrhh_payload(payload)
    vigente = load_rrhh_personal_vigente()
    initial = default_rrhh_payload()

    for row in iter_rrhh_rows():
        key = row["key"]
        previous = historical.get(key, {})
        master_name = _clean(vigente.get(key, ""))
        historical_name = _clean(previous.get("nombre"))
        initial[key] = {
            # Prioridad de nombre RRHH:
            # 1) JSON maestro si trae valor
            # 2) Ultimo reporte si JSON viene en blanco
            "nombre": master_name or historical_name,
            "medio": _clean(previous.get("medio")) or row.get("medio_default", ""),
            "observacion": _clean(previous.get("observacion")),
        }
    return initial


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
