"""
Módulo de alertas e regras de decisão do EnviroSat.

Toda a lógica de threshold está implementada em Python —
a IA interpreta e contextualiza, mas NUNCA decide se há alerta.
"""

# ── Thresholds por parâmetro ──────────────────────────────────────────────────
# Para sensor_termico, buffer_imagens e precisao_geolocalizacao:
#   valor acima do threshold de alerta  → ALERTA
#   valor acima do threshold crítico    → CRITICO
#
# Para sensor_optico_ndvi e energia_disponivel (lógica invertida):
#   valor abaixo do threshold de alerta → ALERTA
#   valor abaixo do threshold crítico   → CRITICO

THRESHOLDS = {
    "sensor_termico": {
        "alerta":  45.0,   # °C
        "critico": 65.0,   # °C
    },
    "sensor_optico_ndvi": {
        "alerta":  80.0,   # % — abaixo disso é degradação
        "critico": 60.0,   # % — abaixo disso é crítico
    },
    "buffer_imagens": {
        "alerta":  50.0,   # %
        "critico": 75.0,   # %
    },
    "precisao_geolocalizacao": {
        "alerta":  10.0,   # metros
        "critico": 25.0,   # metros
    },
    "energia_disponivel": {
        "alerta":  40.0,   # % — abaixo disso é baixa carga
        "critico": 20.0,   # % — abaixo disso ativa modo economia
    },
}


def avaliar(dados):
    """
    Avalia os dados de telemetria e retorna uma lista de alertas.
    Cada alerta é um dicionário com: nivel, parametro, valor, mensagem.
    Retorna lista vazia se todos os sistemas estiverem nominais.
    """
    alertas = []

    # ── Sensor térmico ────────────────────────────────────────────────────────
    temp = dados["sensor_termico"]
    if temp > THRESHOLDS["sensor_termico"]["critico"]:
        alertas.append({
            "nivel":     "CRITICO",
            "parametro": "sensor_termico",
            "valor":     temp,
            "mensagem":  f"Temperatura crítica ({temp}°C) — possível foco de incêndio detectado",
        })
    elif temp > THRESHOLDS["sensor_termico"]["alerta"]:
        alertas.append({
            "nivel":     "ALERTA",
            "parametro": "sensor_termico",
            "valor":     temp,
            "mensagem":  f"Temperatura elevada ({temp}°C) no sensor térmico",
        })

    # ── Sensor óptico (NDVI) ─────────────────────────────────────────────────
    ndvi = dados["sensor_optico_ndvi"]
    if ndvi < THRESHOLDS["sensor_optico_ndvi"]["critico"]:
        alertas.append({
            "nivel":     "CRITICO",
            "parametro": "sensor_optico_ndvi",
            "valor":     ndvi,
            "mensagem":  f"Qualidade do sensor óptico crítica ({ndvi}%) — imagens comprometidas",
        })
    elif ndvi < THRESHOLDS["sensor_optico_ndvi"]["alerta"]:
        alertas.append({
            "nivel":     "ALERTA",
            "parametro": "sensor_optico_ndvi",
            "valor":     ndvi,
            "mensagem":  f"Qualidade do sensor óptico reduzida ({ndvi}%)",
        })

    # ── Buffer de imagens ────────────────────────────────────────────────────
    buf = dados["buffer_imagens"]
    if buf > THRESHOLDS["buffer_imagens"]["critico"]:
        alertas.append({
            "nivel":     "CRITICO",
            "parametro": "buffer_imagens",
            "valor":     buf,
            "mensagem":  f"Buffer quase cheio ({buf}%) — risco de perda de dados antes do downlink",
        })
    elif buf > THRESHOLDS["buffer_imagens"]["alerta"]:
        alertas.append({
            "nivel":     "ALERTA",
            "parametro": "buffer_imagens",
            "valor":     buf,
            "mensagem":  f"Buffer de imagens acima do recomendado ({buf}%)",
        })

    # ── Precisão de geolocalização ───────────────────────────────────────────
    geo = dados["precisao_geolocalizacao"]
    if geo > THRESHOLDS["precisao_geolocalizacao"]["critico"]:
        alertas.append({
            "nivel":     "CRITICO",
            "parametro": "precisao_geolocalizacao",
            "valor":     geo,
            "mensagem":  f"Precisão de geolocalização crítica ({geo}m) — coordenadas não confiáveis",
        })
    elif geo > THRESHOLDS["precisao_geolocalizacao"]["alerta"]:
        alertas.append({
            "nivel":     "ALERTA",
            "parametro": "precisao_geolocalizacao",
            "valor":     geo,
            "mensagem":  f"Precisão de geolocalização reduzida ({geo}m)",
        })

    # ── Energia disponível ───────────────────────────────────────────────────
    energia = dados["energia_disponivel"]
    if energia < THRESHOLDS["energia_disponivel"]["critico"]:
        alertas.append({
            "nivel":     "CRITICO",
            "parametro": "energia_disponivel",
            "valor":     energia,
            "mensagem":  f"Energia crítica ({energia}%) — modo economia ativado automaticamente",
        })
    elif energia < THRESHOLDS["energia_disponivel"]["alerta"]:
        alertas.append({
            "nivel":     "ALERTA",
            "parametro": "energia_disponivel",
            "valor":     energia,
            "mensagem":  f"Energia abaixo do recomendado ({energia}%)",
        })

    return alertas


def modo_economia_ativo(dados):
    """
    Retorna True se a energia estiver em nível crítico.
    Nesse caso o sistema ativa automaticamente o modo economia,
    suspendendo sensores auxiliares para preservar operação mínima.
    """
    return dados["energia_disponivel"] < THRESHOLDS["energia_disponivel"]["critico"]
