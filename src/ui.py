"""
Interface CLI estilo Claude Code — Mission Control AI · EnviroSat.

Usa Rich para renderização de painéis e prompt-toolkit para input editável.
A lógica de análise é delegada inteiramente ao MissionEngine.
"""
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style
import pyfiglet
from datetime import datetime

console = Console()
session = PromptSession(style=Style.from_dict({"prompt": "#06B6D4 bold"}))


def show_banner():
    """Exibe banner ASCII colorido e painel de boas-vindas."""
    banner = pyfiglet.figlet_format("Mission Control", font="ansi_shadow")
    console.print(Text(banner, style="bold #06B6D4"))
    console.print(Panel.fit(
        "Monitoramento ambiental por satélite · IA generativa via Ollama Cloud\n"
        "Trilha: [bold #4ade80]🌳 EnviroSat — Observação Ambiental[/bold #4ade80]\n"
        "Use [bold]/help[/bold] para ver os comandos · [bold]/exit[/bold] para encerrar\n"
        "Modelo: gpt-oss:120b via Ollama Cloud",
        title="◆ MISSION CONTROL AI",
        border_style="#06B6D4"
    ))


def show_response(texto):
    """Renderiza a resposta da IA (ou do snapshot) em painel com timestamp."""
    agora = datetime.now().strftime("%H:%M")
    console.print(Panel(
        texto,
        title="◆ ARIA — Análise Ambiental",
        subtitle=agora,
        border_style="#06B6D4"
    ))


def show_help():
    """Exibe os comandos disponíveis."""
    console.print(Panel(
        "/status  → Exibe telemetria atual do satélite\n"
        "/about   → Informações do projeto e integrantes\n"
        "/help    → Exibe esta mensagem\n"
        "/clear   → Limpa o terminal\n"
        "/exit    → Encerra o sistema\n\n"
        "Qualquer outra entrada é enviada à IA para análise.",
        title="◆ Comandos disponíveis",
        border_style="#8484A0"
    ))


def show_about():
    """Exibe informações do projeto e integrantes."""
    console.print(Panel(
        "Mission Control AI — [bold #4ade80]EnviroSat[/bold #4ade80]\n"
        "Global Solution 2026.1 · FIAP · Ciência da Computação\n"
        "Disciplina: Prompt Engineering and Artificial Intelligence\n\n"
        "[bold]Integrantes:[/bold]\n"
        "  Wendel Pedro        — RM: 573126\n"
        "  Daniel Alejandro    — RM: 573075\n"
        "  Beatriz da Silva    — RM: 570619",
        title="◆ Sobre o projeto",
        border_style="#8484A0"
    ))


def run_cli(engine):
    """Loop principal da CLI."""
    show_banner()

    # Avisa se o motor ainda não foi implementado
    if not engine.is_ready():
        console.print("  ⚠ Engine status: AGUARDANDO IMPLEMENTAÇÃO ✗\n", style="yellow")

    while True:
        try:
            entrada = session.prompt("❯ ").strip()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[#8484A0]Encerrando Mission Control AI...[/#8484A0]")
            break

        if not entrada:
            continue

        if entrada == "/exit":
            console.print("\n[#8484A0]Encerrando Mission Control AI...[/#8484A0]")
            break
        elif entrada == "/help":
            show_help()
        elif entrada == "/status":
            show_response(engine.status_snapshot())
        elif entrada == "/about":
            show_about()
        elif entrada == "/clear":
            console.clear()
            show_banner()
        else:
            # Qualquer pergunta livre é enviada ao motor de análise com IA
            console.print("  [#8484A0]Consultando ARIA...[/#8484A0]")
            resposta = engine.analyze(entrada)
            show_response(resposta)
