"""
Motor de análise da Mission Control AI — trilha EnviroSat.

Este arquivo combina:
  - A função llm() para comunicação com o modelo via Ollama Cloud
  - A classe MissionEngine que une telemetria, alertas e IA
"""
import os
from ollama import Client
from dotenv import load_dotenv
from pathlib import Path
from src import telemetria, alertas

load_dotenv()

# Identificação da trilha escolhida pelo grupo
TRILHA = "envirosat"

# Configuração do cliente Ollama Cloud
# A chave é lida do arquivo .env — nunca hardcoded no código
client = Client(
    host="https://ollama.com",
    headers={"Authorization": "Bearer " + os.environ.get("OLLAMA_API_KEY", "")}
)


def llm(prompt, system=None, max_tokens=800, temperature=0.3):
    """
    Envia um prompt ao modelo gpt-oss:120b via Ollama Cloud e retorna o texto.

    Parâmetros:
        prompt      : texto principal enviado ao modelo
        system      : system prompt opcional (persona e contexto da missão)
        max_tokens  : limite de tokens na resposta
        temperature : criatividade do modelo (0.3 = mais determinístico)
    """
    mensagens = []
    if system:
        mensagens.append({"role": "system", "content": system})
    mensagens.append({"role": "user", "content": prompt})

    try:
        resposta = client.chat(
            model="gpt-oss:120b",
            messages=mensagens,
            options={"num_predict": max_tokens, "temperature": temperature},
            stream=False
        )
        return resposta["message"]["content"].strip()
    except Exception as e:
        return f"⚠️ Erro ao consultar IA: {e}"


def carregar_system_prompt():
    """Lê o system prompt do arquivo prompts/system_prompt.md."""
    caminho = Path("prompts/system_prompt.md")
    if caminho.exists():
        return caminho.read_text(encoding="utf-8")
    # fallback genérico caso o arquivo não seja encontrado
    return "Você é um assistente de missão espacial ambiental."


class MissionEngine:
    """Motor de análise da missão EnviroSat."""

    def __init__(self):
        self.trilha = TRILHA
        self.system_prompt = carregar_system_prompt()

    def is_ready(self):
        """Retorna True — motor completamente implementado."""
        return True

    def status_snapshot(self):
        """
        Coleta uma leitura de telemetria e retorna um resumo
        formatado do estado atual do satélite.
        Não chama a IA — é uma visualização Python pura.
        """
        dados = telemetria.coletar()
        lista_alertas = alertas.avaliar(dados)
        modo_eco = alertas.modo_economia_ativo(dados)

        linhas = []
        linhas.append("🛰  TELEMETRIA — " + dados["timestamp"])
        linhas.append("─" * 44)
        linhas.append("  Sensor Térmico           : " + str(dados["sensor_termico"]) + "°C")
        linhas.append("  Sensor Óptico (NDVI)      : " + str(dados["sensor_optico_ndvi"]) + "%")
        linhas.append("  Buffer de Imagens         : " + str(dados["buffer_imagens"]) + "%")
        linhas.append("  Precisão de Geolocalização: " + str(dados["precisao_geolocalizacao"]) + "m")
        linhas.append("  Energia Disponível        : " + str(dados["energia_disponivel"]) + "%")
        linhas.append("─" * 44)

        if lista_alertas:
            linhas.append("⚠  " + str(len(lista_alertas)) + " ALERTA(S) ATIVO(S):")
            for a in lista_alertas:
                icone = "🔴" if a["nivel"] == "CRITICO" else "🟡"
                linhas.append("  " + icone + " [" + a["nivel"] + "] " + a["mensagem"])
        else:
            linhas.append("✅  Todos os sistemas NOMINAIS.")

        if modo_eco:
            linhas.append("")
            linhas.append("⚡  MODO ECONOMIA ATIVADO — sensores auxiliares suspensos.")

        return "\n".join(linhas)

    def analyze(self, pergunta_usuario):
        """
        Analisa a pergunta do operador usando telemetria em tempo real + IA generativa.

        Fluxo:
          1. Coletar dados via telemetria.coletar()
          2. Avaliar alertas via alertas.avaliar() — lógica Python pura
          3. Montar prompt com dados + alertas + pergunta
          4. Enviar à IA via llm() com o system prompt carregado
          5. Retornar a resposta
        """
        # 1. Coletar telemetria atual
        dados = telemetria.coletar()

        # 2. Avaliar alertas — toda decisão de threshold é feita em Python
        lista_alertas = alertas.avaliar(dados)
        modo_eco = alertas.modo_economia_ativo(dados)

        # 3. Montar o contexto de telemetria que será injetado no prompt
        linhas = []
        linhas.append("TELEMETRIA ATUAL (" + dados["timestamp"] + "):")
        linhas.append("- Sensor Térmico: " + str(dados["sensor_termico"]) + "°C")
        linhas.append("- Sensor Óptico (NDVI): " + str(dados["sensor_optico_ndvi"]) + "%")
        linhas.append("- Buffer de Imagens: " + str(dados["buffer_imagens"]) + "%")
        linhas.append("- Precisão de Geolocalização: " + str(dados["precisao_geolocalizacao"]) + "m")
        linhas.append("- Energia Disponível: " + str(dados["energia_disponivel"]) + "%")
        linhas.append("")
        linhas.append("ALERTAS ATIVOS (" + str(len(lista_alertas)) + " total):")

        if lista_alertas:
            for a in lista_alertas:
                linhas.append("[" + a["nivel"] + "] " + a["mensagem"])
        else:
            linhas.append("Nenhum alerta — todos os sistemas operando normalmente.")

        if modo_eco:
            linhas.append("")
            linhas.append("⚡ MODO ECONOMIA ATIVADO — sensores não-críticos suspensos.")

        contexto = "\n".join(linhas)

        # A pergunta do operador é adicionada ao final do contexto
        prompt_completo = contexto + "\n\nPERGUNTA DO OPERADOR: " + pergunta_usuario

        # 4. Enviar à IA com o system prompt da missão
        return llm(prompt_completo, system=self.system_prompt)
