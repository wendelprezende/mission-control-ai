"""
Módulo de telemetria simulada do satélite EnviroSat.

Gera dados de 5 parâmetros operacionais com probabilidade ponderada,
simulando um cenário operacional verossímil: maioria do tempo nominal,
com ocorrências periódicas de alertas e situações críticas.
"""
import random
from datetime import datetime


# Ranges de cada parâmetro por nível operacional
# sensor_termico     (°C)  : calor superficial detectado — maior = pior
# sensor_optico_ndvi  (%)  : qualidade do sensor óptico RGB+NIR — menor = pior
# buffer_imagens      (%)  : buffer de armazenamento ocupado — maior = pior
# precisao_geolocalizacao (m): erro médio de coordenada — maior = pior
# energia_disponivel  (%)  : carga das baterias solares — menor = pior

RANGES = {
    "sensor_termico": {
        "nominal":  (20.0, 44.9),
        "alerta":   (45.0, 64.9),
        "critico":  (65.0, 90.0),
    },
    "sensor_optico_ndvi": {
        "nominal":  (80.1, 100.0),
        "alerta":   (60.0, 80.0),
        "critico":  (40.0, 59.9),
    },
    "buffer_imagens": {
        "nominal":  (10.0, 49.9),
        "alerta":   (50.0, 74.9),
        "critico":  (75.0, 95.0),
    },
    "precisao_geolocalizacao": {
        "nominal":  (2.0,  9.9),
        "alerta":   (10.0, 24.9),
        "critico":  (25.0, 40.0),
    },
    "energia_disponivel": {
        "nominal":  (40.1, 100.0),
        "alerta":   (20.0, 40.0),
        "critico":  (5.0,  19.9),
    },
}


def _gerar_valor(parametro):
    """
    Gera um valor para o parâmetro com probabilidade ponderada:
    65% nominal · 25% alerta · 10% crítico.
    """
    sorteio = random.random()
    if sorteio < 0.65:
        nivel = "nominal"
    elif sorteio < 0.90:
        nivel = "alerta"
    else:
        nivel = "critico"
    minimo, maximo = RANGES[parametro][nivel]
    return round(random.uniform(minimo, maximo), 1)


def coletar():
    """
    Coleta e retorna os dados simulados de telemetria do satélite.
    Cada chamada gera uma leitura independente.
    """
    dados = {
        "timestamp":               datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "sensor_termico":          _gerar_valor("sensor_termico"),
        "sensor_optico_ndvi":      _gerar_valor("sensor_optico_ndvi"),
        "buffer_imagens":          _gerar_valor("buffer_imagens"),
        "precisao_geolocalizacao": _gerar_valor("precisao_geolocalizacao"),
        "energia_disponivel":      _gerar_valor("energia_disponivel"),
    }
    return dados
