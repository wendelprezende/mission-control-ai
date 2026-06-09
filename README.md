# 🚀 Mission Control AI — EnviroSat

# Integrantes
- Wendel Pedro — RM: 573126 — Turma: 1CCPK
- Daniel Alejandro — RM: 573075 — Turma: 1CCPK
- Beatriz da Silva — RM: 570619 — Turma: 1CCPK

**Modalidade:** Trio

---

# O que o projeto faz

Mission Control AI — EnviroSat é um sistema de monitoramento operacional de um satélite ambiental simulado, desenvolvido em Python com interface CLI. O sistema gera dados de telemetria em tempo real (temperatura de sensor, qualidade óptica, buffer de imagens, geolocalização e energia), detecta anomalias via lógica Python e usa IA generativa (Ollama Cloud, modelo gpt-oss:120b) para interpretar o estado da missão e gerar diagnósticos em linguagem natural. A IA atua como assistente ARIA (Análise e Resposta Inteligente Ambiental), sempre conectando cada anomalia técnica ao seu impacto concreto no monitoramento ambiental brasileiro.

---

# Persona atendida

**Operador de centro de controle ambiental (INPE/órgão estadual)** — responsável por garantir a disponibilidade dos dados do satélite para os sistemas DETER e PRODES. Precisa de diagnósticos precisos em tempo real para decidir ações corretivas antes que falhas comprometam o fluxo de imagens que alimenta brigadas de incêndio e fiscalização ambiental.

---

# Tecnologias utilizadas

- Python 3.10+
- Ollama Cloud API (modelo gpt-oss:120b)
- Bibliotecas: ollama, python-dotenv, rich, prompt_toolkit, pyfiglet

---

# Como executar

1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/mission-control-ai.git
cd mission-control-ai
```

2. Crie o ambiente virtual e ative
```bash
python -m venv .venv
source .venv/bin/activate        # Linux/macOS
.venv\Scripts\activate           # Windows
```

3. Instale as dependências
```bash
pip install -r requirements.txt
```

4. Crie o arquivo `.env` na raiz com:
```
OLLAMA_API_KEY=sua_chave_aqui
```

5. Execute o sistema
```bash
python main.py
```

---

# Demonstração

![Status normal da missão](assets/screenshot_normal.png)

![Alerta crítico com análise da IA](assets/screenshot_alerta.png)

---

# System Prompt

O system prompt completo está em [`prompts/system_prompt.md`](prompts/system_prompt.md).

Resumo: a IA assume o papel de ARIA, assistente de missão do EnviroSat, com contexto completo dos 5 parâmetros monitorados, das 3 personas atendidas (operador INPE, coordenador de brigada, analista de compliance) e das regras de resposta — sempre abrindo com o status geral e terminando com uma recomendação de ação concreta.

---

# Cenários de teste demonstrados

1. **Operação normal** — todos os parâmetros dentro dos ranges nominais; ARIA confirma normalidade e destaca o que está sendo monitorado.
2. **Foco de incêndio detectado** — sensor térmico acima de 65°C; ARIA alerta coordenador de brigada com diagnóstico e recomendação de deslocamento.
3. **Energia crítica** — energia abaixo de 20%; modo economia ativado automaticamente; ARIA comunica quais sensores foram suspensos.
4. **Buffer cheio + geolocalização degradada** — dois alertas simultâneos; ARIA prioriza o que é mais urgente operacionalmente.

---

# Limitações conhecidas

- Os dados de telemetria são gerados aleatoriamente — não há integração com dados reais de satélite.
- O sistema não persiste histórico entre sessões; cada execução começa do zero.
- A resposta da IA pode variar entre chamadas para o mesmo cenário (comportamento esperado em modelos de linguagem).
- Requer conexão com a internet para acessar a Ollama Cloud API.

---

# 💼 Proposta de valor / modelo de negócio

**1. Qual o problema real terrestre que esta missão resolve?**
O Brasil perde anualmente áreas equivalentes a países inteiros para desmatamento e incêndios — a maioria detectada com horas ou dias de atraso por falta de monitoramento contínuo. O EnviroSat resolve esse gap: fornece alertas de foco de incêndio e degradação vegetal em tempo próximo ao real, permitindo que brigadas cheguem antes que o fogo se alastre e que o IBAMA autue antes que a área seja irreversivelmente desmatada.

**2. Quem paga pela solução?**
Modelo híbrido: o setor público (INPE, IBAMA, secretarias estaduais de meio ambiente) paga pela operação básica via contratos de concessão ou parceria com a AEB. O setor privado (cooperativas do agronegócio, empresas com obrigações de compliance ambiental, seguradoras rurais) assina o serviço de dados para relatórios CAR e licenciamento — gerando receita complementar que subsidia o acesso público.

**3. Métrica de impacto**
Se o EnviroSat operar com disponibilidade acima de 95% por 1 ano, o sistema é capaz de monitorar aproximadamente 850.000 km² de áreas protegidas por ciclo orbital, reduzir em até 40% o tempo médio de resposta a focos de incêndio (de ~18h para ~11h) e gerar dados para mais de 12.000 relatórios de compliance ambiental anuais.

**4. Modelo de negócio**
Dado-como-serviço (DaaS) com duas camadas: (a) acesso institucional via API para órgãos públicos em modelo de concessão pública; (b) assinatura SaaS para empresas privadas com dashboard de compliance e alertas customizados por propriedade rural ou bioma monitorado.

---

# 🎬 Vídeo de demonstração

[https://youtu.be/_FTNPDVRrEk](https://youtu.be/_FTNPDVRrEk)

> Configurado como "Não listado" no YouTube.
