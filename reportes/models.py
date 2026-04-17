from django.db import models

# Create your models here.

class Reporte(models.Model):
    OPTIONS = [
        ('option1', 'Opcion 1'),
        ('option2', 'Opcion 2'),
        ('option3', 'Opcion 3'),
    ]
    IGP_OPTIONS = [
        ('BAJO', 'BAJO'),
        ('MEDIO', 'MEDIO'),
        ('ALTO', 'ALTO'),
        ('EXTREMO', 'EXTREMO'),
    ]
    NVL_ALERT_OPTIONS = [
        ('VERDE', 'VERDE'),
        ('AMBAR 1', 'AMBAR 1'),
        ('AMBAR 2', 'AMBAR 2'),
        ('AMBAR 3', 'AMBAR 3'),
        ('ROJO 1', 'ROJO 1'),
        ('ROJO 2', 'ROJO 2'),
    ]

    FACT_SEGURIDAD_OPTIONS = [
        ('BAJO', 'BAJO'),
        ('MEDIO', 'MEDIO'),
        ('REGULAR', 'REGULAR'),
        ('BUENO', 'BUENO')
    ]
    OPTIONS_2 = [
        ('ON', 'ON'),
        ('OFF', 'OFF'),
        ('NO VISIBLE', 'NO VISIBLE'),
    ]

    fecha_hora = models.DateTimeField(auto_now_add=True)

    # Clima (antes CharField(250))
    temperatura = models.TextField(blank=True, null=True)
    viento = models.TextField(blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    humedad = models.TextField(blank=True, null=True)
    precipitaciones_dia = models.TextField(blank=True, null=True)

    igp = models.CharField(max_length=50)
    nvl_alerta = models.CharField(max_length=50)
    factor_seguridad = models.CharField(max_length=50)
    nivel_riesgos_operativos = models.CharField(max_length=50)

    # Clima Lomas (antes CharField(250))
    lomas_temperatura = models.TextField(blank=True, null=True)
    lomas_viento = models.TextField(blank=True, null=True)
    lomas_direccion = models.TextField(blank=True, null=True)
    lomas_humedad = models.TextField(blank=True, null=True)
    lomas_precipitaciones_dia = models.TextField(blank=True, null=True)

    lomas_igp = models.CharField(max_length=50)
    lomas_nvl_alerta = models.CharField(max_length=50)

    # personal turno
    jefe_semana = models.CharField(max_length=100)
    segundo_jefe = models.CharField(max_length=100)
    oficina_ays = models.CharField(max_length=100)
    et_alerta_semana = models.TextField(blank=True, null=True)
    encargado_turno = models.CharField(max_length=100)
    central = models.CharField(max_length=100)
    guardia_seguridad = models.CharField(max_length=100)
    guardia_seguridad2 = models.CharField(max_length=100)
    guardia_seguridad3 = models.CharField(max_length=100)
    relacionador = models.CharField(max_length=100)
    relacionador2 = models.CharField(max_length=100)
    drone = models.CharField(max_length=100)
    drone2 = models.CharField(max_length=100)
    eq_tecnico_1 = models.CharField(max_length=100)
    eq_tecnico_2 = models.CharField(max_length=100)
    brigada_if = models.CharField(max_length=100)

    ml_jefe_semana = models.CharField(max_length=100)
    ml_segundo_jefe = models.CharField(max_length=100)
    ml_oficina_ays = models.CharField(max_length=100)
    ml_et_alerta_semana = models.TextField(blank=True, null=True)
    ml_encargado_turno = models.CharField(max_length=100)
    ml_central = models.CharField(max_length=100)
    ml_guardia_seguridad = models.CharField(max_length=100)
    ml_guardia_seguridad2 = models.CharField(max_length=100)
    ml_guardia_seguridad3 = models.CharField(max_length=100)
    ml_relacionador = models.CharField(max_length=100)
    ml_relacionador2 = models.CharField(max_length=100)
    ml_drone = models.CharField(max_length=100)
    ml_drone2 = models.CharField(max_length=100)
    ml_eq_tecnico_1 = models.CharField(max_length=100)
    ml_eq_tecnico_2 = models.CharField(max_length=100)
    ml_brigada_if = models.CharField(max_length=100)

    # RRHH (estructura dinamica desde tabla excel)
    rrhh_registros = models.JSONField(blank=True, default=dict)

    # vehiculos comunidad
    movil_13_stado = models.CharField(max_length=100)
    movil_11_stado = models.CharField(max_length=100)
    movil_14_stado = models.CharField(max_length=100)

    movil_13_odometro = models.IntegerField(blank=True, null=True)
    movil_11_odometro = models.IntegerField(blank=True, null=True)
    movil_14_odometro = models.IntegerField(blank=True, null=True)

    # Eléctrico (antes CharField(250))
    elect_central_l1 = models.TextField(blank=True, null=True)
    elect_central_l2 = models.TextField(blank=True, null=True)
    elect_central_l3 = models.TextField(blank=True, null=True)
    elect_ghr_l1 = models.TextField(blank=True, null=True)
    elect_ghr_l2 = models.TextField(blank=True, null=True)
    elect_ghr_l3 = models.TextField(blank=True, null=True)
    elect_lomas_l1 = models.TextField(blank=True, null=True)
    elect_lomas_l2 = models.TextField(blank=True, null=True)
    elect_lomas_l3 = models.TextField(blank=True, null=True)

    solar_central_3led_izq = models.CharField(max_length=100)
    solar_ghr_3led_der = models.CharField(max_length=100)
    solar_lomas_led_amarillo = models.CharField(max_length=100)
    inversor_central_izq = models.CharField(max_length=100)
    inversor_ghr_medio = models.CharField(max_length=100)
    inversor_lomas_derecho = models.CharField(max_length=100)

    indicar_cual_cctv = models.CharField(max_length=255, blank=True, default="Todas apagadas")
    alarma_ugps_activa = models.CharField(max_length=255, blank=True, null=True)
    cctv_sistema_o = models.CharField(max_length=100, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)

    vuelos_drone = models.IntegerField(blank=True, null=True)
    accesos_extern_turn = models.IntegerField(blank=True, null=True)
    accesos_ventas_dia = models.IntegerField(blank=True, null=True)

    peas_aires = models.CharField(max_length=100)
    cargadero_aires = models.CharField(max_length=100)
    planta_solar = models.CharField(max_length=100, blank=True, null=True)
    sala_1 = models.CharField(max_length=100)
    sala_2 = models.CharField(max_length=100)
    sala_club2 = models.CharField(max_length=100)
    estanques_x = models.CharField(max_length=100)
    mestiza_belloto = models.CharField(max_length=100)
    elevadora_gh = models.CharField(max_length=100)
    lomas_acceso = models.CharField(max_length=100, blank=True, null=True)
    lomas = models.CharField(max_length=100)
    otras = models.CharField(max_length=100)

    otras_novedades = models.TextField(blank=True, null=True)

    obs_vuelos_drone = models.CharField(max_length=100)
    obs_accesos_extern_turn = models.CharField(max_length=100)
    obs_accesos_ventas_dia = models.CharField(max_length=100)

    # obs_* (antes CharField(255))
    obs_peas_aires = models.TextField(blank=True, null=True)
    obs_cargadero_aires = models.TextField(blank=True, null=True)
    obs_sala_1 = models.TextField(blank=True, null=True)
    obs_sala_2 = models.TextField(blank=True, null=True)
    obs_sala_club2 = models.TextField(blank=True, null=True)
    obs_estanques_x = models.TextField(blank=True, null=True)
    obs_mestiza_belloto = models.TextField(blank=True, null=True)
    obs_elevadora_gh = models.TextField(blank=True, null=True)
    obs_lomas_acceso = models.TextField(blank=True, null=True)
    sistema_o = models.CharField(max_length=100, blank=True, null=True)
    obs_sistema_o = models.TextField(blank=True, null=True)
    obs_lomas = models.TextField(blank=True, null=True)
    obs_otras = models.TextField(blank=True, null=True)
    baliza_encendida_lomas_acceso = models.CharField(max_length=10, blank=True, null=True)
    baliza_encendida_lomas = models.CharField(max_length=10, blank=True, null=True)

    confirmado = models.BooleanField(default=False)

    porton_mestiza = models.CharField(max_length=100)
    porton_ghr = models.CharField(max_length=100)
    porton_cargadero = models.CharField(max_length=100)

    # Portones (antes CharField(250))
    porton_mestiza_observaciones = models.TextField(blank=True, null=True)
    porton_ghr_observaciones = models.TextField(blank=True, null=True)
    porton_cargadero_observaciones = models.TextField(blank=True, null=True)

    porton_i = models.TextField(blank=True, null=True)
    porton_norte = models.TextField(blank=True, null=True)
    sala_mestiza = models.TextField(blank=True, null=True)

    porton_i_observaciones = models.TextField(blank=True, null=True)
    porton_norte_observaciones = models.TextField(blank=True, null=True)
    sala_mestiza_observaciones = models.TextField(blank=True, null=True)

    # nuevas balizas
    pozo_ch1 = models.CharField(max_length=100)
    planta_mirador_gh = models.CharField(max_length=100)
    pozo_p7 = models.CharField(max_length=100)
    diamante_1 = models.CharField(max_length=100)
    diamante_2 = models.CharField(max_length=100)
    retamilla_dia_visible = models.CharField(max_length=100)
    retamilla_noche_luz = models.CharField(max_length=100)
    ptas_visible = models.CharField(max_length=100)

    # observaciones balizas (antes CharField(255))
    pozo_ch1_observaciones = models.TextField(blank=True, null=True)
    planta_mirador_gh_observaciones = models.TextField(blank=True, null=True)
    pozo_p7_observaciones = models.TextField(blank=True, null=True)
    diamante_1_observaciones = models.TextField(blank=True, null=True)
    diamante_2_observaciones = models.TextField(blank=True, null=True)
    retamilla_dia_visible_observaciones = models.TextField(blank=True, null=True)
    retamilla_noche_luz_observaciones = models.TextField(blank=True, null=True)
    ptas_visible_observaciones = models.TextField(blank=True, null=True)

    # NUEVA SECCION PRESIONES
    presion_lomas = models.CharField(max_length=100)
    presion_gh = models.CharField(max_length=100, blank=True, null=True)
    sm_ch2 = models.CharField(max_length=100)
    sm_3 = models.CharField(max_length=100)
    sm_1 = models.CharField(max_length=100)
    torre_y = models.CharField(max_length=100)

    # presiones obs (antes CharField(255))
    presion_lomas_obs = models.TextField(blank=True, null=True)
    presion_gh_obs = models.TextField(blank=True, null=True)
    sm_ch2_obs = models.TextField(blank=True, null=True)
    sm_3_obs = models.TextField(blank=True, null=True)
    sm_1_obs = models.TextField(blank=True, null=True)
    torre_y_obs = models.TextField(blank=True, null=True)

    # NUEVAS LECTURAS (antes CharField(250))
    sm_3_l1 = models.TextField(blank=True, null=True)
    sm_3_l2 = models.TextField(blank=True, null=True)
    sm_3_l3 = models.TextField(blank=True, null=True)

    sm_1_l1 = models.TextField(blank=True, null=True)
    sm_1_l2 = models.TextField(blank=True, null=True)
    sm_1_l3 = models.TextField(blank=True, null=True)

    torre_y_l1 = models.TextField(blank=True, null=True)
    torre_y_l2 = models.TextField(blank=True, null=True)
    torre_y_l3 = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Reporte creado el {self.fecha_hora}'


class RRHHPersonalVigente(models.Model):
    row_key = models.CharField(max_length=100, unique=True)
    nombre_vigente = models.CharField(max_length=150, blank=True, default="")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["row_key"]
        verbose_name = "Personal RRHH vigente"
        verbose_name_plural = "Personal RRHH vigente"

    def __str__(self):
        return f"{self.row_key}: {self.nombre_vigente or '(sin nombre)'}"
