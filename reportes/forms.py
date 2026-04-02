from django import forms

from .models import Reporte
from .rrhh import RRHH_SECTIONS, iter_rrhh_rows, normalize_rrhh_payload


IGP_OPTIONS = [
    ("BAJO", "BAJO"),
    ("MEDIO", "MEDIO"),
    ("ALTO", "ALTO"),
    ("EXTREMO", "EXTREMO"),
]

NVL_ALERT_OPTIONS = [
    ("VERDE", "VERDE"),
    ("AMBAR 1", "AMBAR 1"),
    ("AMBAR 2", "AMBAR 2"),
    ("AMBAR 3", "AMBAR 3"),
    ("ROJO 1", "ROJO 1"),
    ("ROJO 2", "ROJO 2"),
]

FACT_SEGURIDAD_OPTIONS = [
    ("BAJO", "BAJO"),
    ("MEDIO", "MEDIO"),
    ("REGULAR", "REGULAR"),
    ("BUENO", "BUENO"),
]

OPCIONES_ML = [
    ("CENTRAL", "CENTRAL"),
    ("ET TURNO", "ET TURNO"),
    ("LLAMADO", "LLAMADO"),
    ("MOVIL 13", "MOVIL 13"),
    ("MOVIL 81", "MOVIL 81"),
    ("ARRIENDO", "ARRIENDO"),
    ("DSFK (CHINA)", "DSFK (CHINA)"),
    ("P NORTE", "P NORTE"),
    ("P. GHR", "P. GHR"),
    ("P SUR", "P SUR"),
    ("TORRE X", "TORRE X"),
    ("TORRE 10", "TORRE 10"),
    ("TORRE Y", "TORRE Y"),
    ("CLUB 1 - OF ADM", "CLUB 1 - OF ADM"),
    ("CLUB 2", "CLUB 2"),
    ("Cuartel 2", "Cuartel 2"),
    ("Torre Q", "Torre Q"),
    ("Otro", "Otro"),
]

OPTIONS2 = [
    ("ON", "ON"),
    ("OFF", "OFF"),
    ("NO VISIBLE", "NO VISIBLE"),
]

OPTIONS3 = [
    ("ON", "ON"),
    ("OFF", "OFF"),
    ("No visible - Sin imagen ", "No visible - Sin imagen "),
]

OPTIONS4 = [
    ("ABIERTO", "ABIERTO"),
    ("CERRADO", "CERRADO"),
]

OPTIONS5 = [
    ("0", "0"),
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("4", "4"),
    ("5", "5"),
    ("Sin Vision", "Sin Vision"),
]

OPTIONS6 = [
    ("Fuera de servicio", "Fuera de servicio"),
    ("Operativo", "Operativo"),
    ("En reparacion", "En reparacion"),
]


class ReportForm(forms.ModelForm):
    NON_NEGATIVE_FIELDS = (
        "movil_13_odometro",
        "movil_11_odometro",
        "movil_14_odometro",
        "vuelos_drone",
        "accesos_extern_turn",
        "accesos_ventas_dia",
    )

    temperatura = forms.CharField(label="Temperatura", required=False)
    viento = forms.CharField(label="Viento", required=False)
    direccion = forms.CharField(label="Direccion del viento", required=False)
    humedad = forms.CharField(label="Humedad", required=False)
    precipitaciones_dia = forms.CharField(label="Precipitaciones dia", required=False)

    igp = forms.ChoiceField(choices=IGP_OPTIONS, widget=forms.RadioSelect(), label="IGP")
    nvl_alerta = forms.ChoiceField(
        choices=NVL_ALERT_OPTIONS, widget=forms.RadioSelect(), label="Nivel de alerta"
    )
    factor_seguridad = forms.ChoiceField(
        choices=FACT_SEGURIDAD_OPTIONS, widget=forms.RadioSelect(), label="Factor seguridad"
    )
    nivel_riesgos_operativos = forms.ChoiceField(
        choices=FACT_SEGURIDAD_OPTIONS,
        widget=forms.RadioSelect(),
        label="Nivel riesgos operativos",
    )

    lomas_temperatura = forms.CharField(label="Lomas Temperatura", required=False)
    lomas_viento = forms.CharField(label="Lomas Viento", required=False)
    lomas_direccion = forms.CharField(label="Lomas Direccion del viento", required=False)
    lomas_humedad = forms.CharField(label="Lomas Humedad", required=False)
    lomas_precipitaciones_dia = forms.CharField(label="Lomas Precipitaciones dia", required=False)

    lomas_igp = forms.ChoiceField(choices=IGP_OPTIONS, widget=forms.RadioSelect(), label="Lomas IGP")
    lomas_nvl_alerta = forms.ChoiceField(
        choices=NVL_ALERT_OPTIONS, widget=forms.RadioSelect(), label="Lomas Nivel de alerta"
    )

    jefe_semana = forms.CharField(max_length=100, label="Jefe Semana", required=False)
    ml_jefe_semana = forms.ChoiceField(choices=OPCIONES_ML, label="Medio/Lugar", required=False)

    segundo_jefe = forms.CharField(max_length=100, label="Supervisor COM", required=False)
    ml_segundo_jefe = forms.ChoiceField(choices=OPCIONES_ML, label="Medio/Lugar", required=False)

    oficina_ays = forms.CharField(max_length=100, label="Oficina AyS", required=False)
    ml_oficina_ays = forms.ChoiceField(choices=OPCIONES_ML, label="Medio/Lugar", required=False)

    et_alerta_semana = forms.CharField(max_length=100, label="ET alerta semana", required=False)
    ml_et_alerta_semana = forms.ChoiceField(choices=OPCIONES_ML, label="Medio/Lugar", required=False)

    encargado_turno = forms.CharField(max_length=100, label="Encargado Turno", required=False)
    ml_encargado_turno = forms.ChoiceField(choices=OPCIONES_ML, label="Medio/Lugar")

    central = forms.CharField(max_length=100, label="Central", required=False)
    ml_central = forms.ChoiceField(choices=OPCIONES_ML, label="Medio/Lugar")

    guardia_seguridad = forms.CharField(max_length=100, label="Guardia de seguridad", required=False)
    ml_guardia_seguridad = forms.ChoiceField(choices=OPCIONES_ML, label="Medio/Lugar")

    guardia_seguridad2 = forms.CharField(max_length=100, label="Guardia de seguridad 2", required=False)
    ml_guardia_seguridad2 = forms.ChoiceField(choices=OPCIONES_ML, label="Medio/Lugar")

    guardia_seguridad3 = forms.CharField(max_length=100, label="Guardia de seguridad 3", required=False)
    ml_guardia_seguridad3 = forms.ChoiceField(choices=OPCIONES_ML, label="Medio/Lugar")

    relacionador = forms.CharField(max_length=100, label="Relacionador", required=False)
    ml_relacionador = forms.ChoiceField(choices=OPCIONES_ML, label="Medio/Lugar")

    relacionador2 = forms.CharField(max_length=100, label="Relacionador 2", required=False)
    ml_relacionador2 = forms.ChoiceField(choices=OPCIONES_ML, label="Medio/Lugar")

    drone = forms.CharField(max_length=100, label="Drone 1", required=False)
    ml_drone = forms.ChoiceField(choices=OPCIONES_ML, label="Medio/Lugar")

    drone2 = forms.CharField(max_length=100, label="Drone 2", required=False)
    ml_drone2 = forms.ChoiceField(choices=OPCIONES_ML, label="Medio/Lugar")

    eq_tecnico_1 = forms.CharField(max_length=100, label="EQ Tecnico 1", required=False)
    ml_eq_tecnico_1 = forms.ChoiceField(choices=OPCIONES_ML, label="Medio/Lugar")

    eq_tecnico_2 = forms.CharField(max_length=100, label="EQ Tecnico 2", required=False)
    ml_eq_tecnico_2 = forms.ChoiceField(choices=OPCIONES_ML, label="Medio/Lugar")

    brigada_if = forms.CharField(max_length=100, label="Brigada IF", required=False)
    ml_brigada_if = forms.ChoiceField(choices=OPCIONES_ML, label="Medio/Lugar")

    movil_13_stado = forms.ChoiceField(
        choices=OPTIONS6, widget=forms.RadioSelect(), label="Movil 13 Estado", required=False
    )
    movil_13_odometro = forms.IntegerField(label="Movil 13 Odometro (KMS)", required=False)
    movil_11_stado = forms.ChoiceField(
        choices=OPTIONS6, widget=forms.RadioSelect(), label="Movil 81 Estado", required=False
    )
    movil_11_odometro = forms.IntegerField(label="Movil 81 Odometro (KMS)", required=False)
    movil_14_stado = forms.ChoiceField(
        choices=OPTIONS6, widget=forms.RadioSelect(), label="Arriendo Estado", required=False
    )
    movil_14_odometro = forms.IntegerField(label="Arriendo Odometro (KMS)", required=False)

    elect_central_l1 = forms.CharField(label="Central L1")
    elect_central_l2 = forms.CharField(label="Central L2")
    elect_central_l3 = forms.CharField(label="Central L3")
    elect_ghr_l1 = forms.CharField(label="GHR L1")
    elect_ghr_l2 = forms.CharField(label="GHR L2")
    elect_ghr_l3 = forms.CharField(label="GHR L3")
    elect_lomas_l1 = forms.CharField(label="Lomas L1")
    elect_lomas_l2 = forms.CharField(label="Lomas L2")
    elect_lomas_l3 = forms.CharField(label="Lomas L3")

    solar_central_3led_izq = forms.ChoiceField(
        choices=OPTIONS2, widget=forms.RadioSelect(), label="SOLAR CENTRAL (3LED IZQ)"
    )
    solar_ghr_3led_der = forms.ChoiceField(
        choices=OPTIONS2, widget=forms.RadioSelect(), label="SOLAR GHR (3LED DER)"
    )
    solar_lomas_led_amarillo = forms.ChoiceField(
        choices=OPTIONS2, widget=forms.RadioSelect(), label="SOLAR LOMAS (LED AMARILLO)"
    )
    inversor_central_izq = forms.ChoiceField(
        choices=OPTIONS2, widget=forms.RadioSelect(), label="INVERSOR CENTRAL (IZQ)"
    )
    inversor_ghr_medio = forms.ChoiceField(
        choices=OPTIONS2, widget=forms.RadioSelect(), label="INVERSOR GHR (3LED IZQ)"
    )
    inversor_lomas_derecho = forms.ChoiceField(
        choices=OPTIONS2, widget=forms.RadioSelect(), label="INVERSOR LOMAS (DER)"
    )

    indicar_cual_cctv = forms.CharField(
        required=False,
        label="ALARMA UGPS ACTIVADA",
        initial="Todas apagadas",
        widget=forms.TextInput(attrs={"placeholder": "Todas apagadas"}),
    )
    cctv_sistema_o = forms.ChoiceField(
        choices=OPTIONS3,
        widget=forms.RadioSelect(),
        label="CCTV SISTEMA O",
        required=False,
    )
    observaciones = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 3}),
        help_text="Indica observaciones de CCTV (incluye Sistema O si aplica).",
    )

    vuelos_drone = forms.IntegerField(label="VUELOS DRONE DIA", required=False)
    accesos_extern_turn = forms.IntegerField(label="ACCESOS EXTERNOS TURNO", required=False)
    accesos_ventas_dia = forms.IntegerField(label="ACCESOS VENTAS DIA", required=False)

    peas_aires = forms.ChoiceField(choices=OPTIONS3, widget=forms.RadioSelect(), required=False)
    cargadero_aires = forms.ChoiceField(choices=OPTIONS3, widget=forms.RadioSelect(), required=False)
    sala_1 = forms.ChoiceField(choices=OPTIONS3, widget=forms.RadioSelect(), required=False)
    sala_2 = forms.ChoiceField(choices=OPTIONS3, widget=forms.RadioSelect(), required=False)
    sala_club2 = forms.ChoiceField(choices=OPTIONS3, widget=forms.RadioSelect(), required=False)
    estanques_x = forms.ChoiceField(choices=OPTIONS3, widget=forms.RadioSelect(), required=False)
    mestiza_belloto = forms.ChoiceField(choices=OPTIONS3, widget=forms.RadioSelect(), required=False)
    elevadora_gh = forms.ChoiceField(choices=OPTIONS3, widget=forms.RadioSelect(), required=False)
    lomas = forms.ChoiceField(choices=OPTIONS3, widget=forms.RadioSelect(), required=False)

    pozo_ch1 = forms.ChoiceField(choices=OPTIONS3, widget=forms.RadioSelect(), required=False)
    planta_mirador_gh = forms.ChoiceField(choices=OPTIONS3, widget=forms.RadioSelect(), required=False)
    pozo_p7 = forms.ChoiceField(choices=OPTIONS3, widget=forms.RadioSelect(), required=False)
    diamante_1 = forms.ChoiceField(choices=OPTIONS3, widget=forms.RadioSelect(), required=False)
    diamante_2 = forms.ChoiceField(choices=OPTIONS3, widget=forms.RadioSelect(), required=False)
    retamilla_dia_visible = forms.ChoiceField(choices=OPTIONS3, widget=forms.RadioSelect(), required=False)
    retamilla_noche_luz = forms.ChoiceField(choices=OPTIONS3, widget=forms.RadioSelect(), required=False)
    ptas_visible = forms.ChoiceField(choices=OPTIONS3, widget=forms.RadioSelect(), required=False)

    pozo_ch1_observaciones = forms.CharField(max_length=255, label="OBSERVACIONES", required=False)
    planta_mirador_gh_observaciones = forms.CharField(
        max_length=255, label="OBSERVACIONES", required=False
    )
    pozo_p7_observaciones = forms.CharField(max_length=255, label="OBSERVACIONES", required=False)
    diamante_1_observaciones = forms.CharField(max_length=255, label="OBSERVACIONES", required=False)
    diamante_2_observaciones = forms.CharField(max_length=255, label="OBSERVACIONES", required=False)
    retamilla_dia_visible_observaciones = forms.CharField(
        max_length=255, label="OBSERVACIONES", required=False
    )
    retamilla_noche_luz_observaciones = forms.CharField(
        max_length=255, label="OBSERVACIONES", required=False
    )
    ptas_visible_observaciones = forms.CharField(max_length=255, label="OBSERVACIONES", required=False)

    otras = forms.ChoiceField(choices=OPTIONS3, widget=forms.RadioSelect(), required=False)
    otras_novedades = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 3}),
        help_text="Deja en blanco si no hay novedades.",
    )

    obs_vuelos_drone = forms.CharField(max_length=100, label="OBSERVACIONES", required=False)
    obs_accesos_extern_turn = forms.CharField(max_length=100, label="OBSERVACIONES", required=False)
    obs_accesos_ventas_dia = forms.CharField(max_length=100, label="OBSERVACIONES", required=False)

    obs_peas_aires = forms.CharField(max_length=100, label="OBSERVACIONES", required=False)
    obs_cargadero_aires = forms.CharField(max_length=100, label="OBSERVACIONES", required=False)
    obs_sala_1 = forms.CharField(max_length=100, label="OBSERVACIONES", required=False)
    obs_sala_2 = forms.CharField(max_length=100, label="OBSERVACIONES", required=False)
    obs_sala_club2 = forms.CharField(max_length=100, label="OBSERVACIONES", required=False)
    obs_estanques_x = forms.CharField(max_length=100, label="OBSERVACIONES", required=False)
    obs_mestiza_belloto = forms.CharField(max_length=100, label="OBSERVACIONES", required=False)
    obs_elevadora_gh = forms.CharField(max_length=100, label="OBSERVACIONES", required=False)
    sistema_o = forms.ChoiceField(choices=OPTIONS3, widget=forms.RadioSelect(), required=False)
    obs_sistema_o = forms.CharField(max_length=100, label="OBSERVACIONES", required=False)
    obs_lomas = forms.CharField(max_length=100, label="OBSERVACIONES", required=False)
    obs_otras = forms.CharField(max_length=100, label="OBSERVACIONES", required=False)

    porton_mestiza = forms.ChoiceField(choices=OPTIONS4, widget=forms.RadioSelect(), label="Mestiza")
    porton_ghr = forms.ChoiceField(choices=OPTIONS4, widget=forms.RadioSelect(), label="GHR")
    porton_cargadero = forms.ChoiceField(choices=OPTIONS4, widget=forms.RadioSelect(), label="CARGADERO")

    porton_mestiza_observaciones = forms.CharField(max_length=250, required=False)
    porton_ghr_observaciones = forms.CharField(max_length=250, required=False)
    porton_cargadero_observaciones = forms.CharField(max_length=250, required=False)

    porton_i = forms.ChoiceField(choices=OPTIONS4, widget=forms.RadioSelect(), label="Porton I")
    porton_norte = forms.ChoiceField(choices=OPTIONS4, widget=forms.RadioSelect(), label="Porton Norte")
    sala_mestiza = forms.ChoiceField(choices=OPTIONS4, widget=forms.RadioSelect(), label="Sala Mestiza")

    porton_i_observaciones = forms.CharField(max_length=250, required=False)
    porton_norte_observaciones = forms.CharField(max_length=250, required=False)
    sala_mestiza_observaciones = forms.CharField(max_length=250, required=False)

    presion_lomas = forms.ChoiceField(choices=OPTIONS5, widget=forms.RadioSelect(), label="Presion Lomas")
    presion_gh = forms.ChoiceField(choices=OPTIONS5, widget=forms.RadioSelect(), label="Presion GH")
    sm_ch2 = forms.ChoiceField(choices=OPTIONS5, widget=forms.RadioSelect(), label="SM CH2")
    sm_3 = forms.ChoiceField(choices=OPTIONS5, widget=forms.RadioSelect(), label="SM 3")
    sm_1 = forms.ChoiceField(choices=OPTIONS5, widget=forms.RadioSelect(), label="SM 1")
    torre_y = forms.ChoiceField(choices=OPTIONS5, widget=forms.RadioSelect(), label="TORRE Y")

    presion_lomas_obs = forms.CharField(max_length=250, required=False)
    presion_gh_obs = forms.CharField(max_length=250, required=False)
    sm_ch2_obs = forms.CharField(max_length=250, required=False)
    sm_3_obs = forms.CharField(max_length=250, required=False)
    sm_1_obs = forms.CharField(max_length=250, required=False)
    torre_y_obs = forms.CharField(max_length=250, required=False)

    sm_3_l1 = forms.CharField(label="SM 3 L1")
    sm_3_l2 = forms.CharField(label="SM 3 L2")
    sm_3_l3 = forms.CharField(label="SM 3 L3")

    sm_1_l1 = forms.CharField(label="SM 1 L1")
    sm_1_l2 = forms.CharField(label="SM 1 L2")
    sm_1_l3 = forms.CharField(label="SM 1 L3")

    torre_y_l1 = forms.CharField(label="TORRE Y L1")
    torre_y_l2 = forms.CharField(label="TORRE Y L2")
    torre_y_l3 = forms.CharField(label="TORRE Y L3")

    class Meta:
        model = Reporte
        fields = "__all__"

    @staticmethod
    def _rrhh_field_names(row_key):
        return (
            f"rrhh_{row_key}_nombre",
            f"rrhh_{row_key}_medio",
            f"rrhh_{row_key}_observacion",
        )

    def _build_rrhh_dynamic_fields(self):
        rrhh_payload = normalize_rrhh_payload(getattr(self.instance, "rrhh_registros", None))
        self.rrhh_sections = []

        for section in RRHH_SECTIONS:
            section_rows = []
            for row in section["rows"]:
                row_key = row["key"]
                nombre_field, medio_field, observacion_field = self._rrhh_field_names(row_key)
                row_data = rrhh_payload.get(row_key, {})

                self.fields[nombre_field] = forms.CharField(required=False, label="Nombre")
                self.fields[medio_field] = forms.CharField(required=False, label="Medio/Lugar")
                self.fields[observacion_field] = forms.CharField(
                    required=False,
                    label="Observacion",
                    widget=forms.TextInput(),
                )

                if not self.is_bound:
                    self.fields[nombre_field].initial = row_data.get("nombre", "")
                    self.fields[medio_field].initial = row_data.get(
                        "medio", row.get("medio_default", "")
                    )
                    self.fields[observacion_field].initial = row_data.get("observacion", "")

                section_rows.append(
                    {
                        "label": row["label"],
                        "nombre_field": nombre_field,
                        "medio_field": medio_field,
                        "observacion_field": observacion_field,
                    }
                )
            self.rrhh_sections.append({"title": section["title"], "rows": section_rows})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._build_rrhh_dynamic_fields()

        for field_name, field in self.fields.items():
            widget = field.widget
            if self.is_bound and field_name in self.errors:
                existing = widget.attrs.get("class", "")
                widget.attrs["class"] = (existing + " is-invalid").strip()

            if isinstance(widget, forms.RadioSelect):
                widget.attrs.setdefault("class", "radio-list")
                continue
            if isinstance(widget, forms.Select):
                widget.attrs.setdefault("class", "form-control input-sm")
                continue
            if isinstance(widget, forms.Textarea):
                widget.attrs.setdefault("class", "form-control")
                widget.attrs.setdefault("placeholder", "Opcional")
                continue
            widget.attrs.setdefault("class", "form-control input-sm")
            if isinstance(widget, forms.NumberInput):
                widget.attrs.setdefault("min", "0")
            if not field.required:
                widget.attrs.setdefault("placeholder", "Opcional")

        self.fields["observaciones"].widget.attrs["placeholder"] = (
            "Observaciones CCTV (ej: Sistema O sin imagen)."
        )
        self.fields["indicar_cual_cctv"].widget.attrs["placeholder"] = "Todas apagadas"

    def clean(self):
        cleaned_data = super().clean()

        for field_name in self.NON_NEGATIVE_FIELDS:
            value = cleaned_data.get(field_name)
            if value is not None and value < 0:
                self.add_error(field_name, "Este valor no puede ser negativo.")

        if not cleaned_data.get("indicar_cual_cctv"):
            cleaned_data["indicar_cual_cctv"] = "Todas apagadas"

        for field_name, value in cleaned_data.items():
            if isinstance(value, str):
                cleaned_data[field_name] = value.strip()

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        rrhh_payload = {}

        for row in iter_rrhh_rows():
            row_key = row["key"]
            nombre_field, medio_field, observacion_field = self._rrhh_field_names(row_key)
            rrhh_payload[row_key] = {
                "nombre": self.cleaned_data.get(nombre_field, ""),
                "medio": self.cleaned_data.get(medio_field, ""),
                "observacion": self.cleaned_data.get(observacion_field, ""),
            }

        instance.rrhh_registros = rrhh_payload

        if commit:
            instance.save()
            self.save_m2m()
        return instance
