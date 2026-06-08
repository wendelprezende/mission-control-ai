"""
Script auxiliar para geração e demonstração do banner ASCII.

Uso:
  python banner_ascii.py               → exibe o banner padrão
  python banner_ascii.py -fonts        → lista todas as fontes disponíveis
  python banner_ascii.py -font slant -text "EnviroSat"  → testa uma fonte
  python banner_ascii.py -demo         → demonstra 8 fontes diferentes
"""
import argparse
import pyfiglet
from rich.console import Console
from rich.align import Align
from rich.text import Text

console = Console()


def exibir_banner_padrao():
    """Exibe o banner padrão do projeto com as duas linhas em cores definidas."""
    linha1 = pyfiglet.figlet_format("Global Solution", font="ansi_shadow")
    linha2 = pyfiglet.figlet_format("Mission Control AI", font="ansi_shadow")
    console.print(Align.center(Text(linha1, style="bold #A855F7")))
    console.print(Align.center(Text(linha2, style="bold #06B6D4")))
    console.print(Align.center(
        Text("── 2026.1 · Prompt Engineering and AI · FIAP ──", style="italic #8484A0")
    ))


def listar_fontes():
    """Lista todas as fontes disponíveis no PyFiglet."""
    fontes = pyfiglet.FigletFont.getFonts()
    console.print("[#06B6D4]Fontes disponíveis (" + str(len(fontes)) + " total):[/#06B6D4]")
    for fonte in sorted(fontes):
        console.print("  " + fonte)


def testar_fonte(fonte, texto):
    """Testa uma fonte específica com o texto fornecido."""
    try:
        resultado = pyfiglet.figlet_format(texto, font=fonte)
        console.print(Text(resultado, style="bold #06B6D4"))
    except pyfiglet.FontNotFound:
        console.print("[red]Fonte '" + fonte + "' não encontrada.[/red]")


def demonstrar_fontes():
    """Demonstra 8 fontes diferentes com o texto 'EnviroSat'."""
    fontes_demo = [
        "ansi_shadow", "slant", "banner3-D", "doom",
        "epic", "isometric1", "larry3d", "roman"
    ]
    texto_demo = "EnviroSat"
    for fonte in fontes_demo:
        console.print("\n[#8484A0]── Fonte: " + fonte + " ──[/#8484A0]")
        try:
            resultado = pyfiglet.figlet_format(texto_demo, font=fonte)
            console.print(Text(resultado, style="bold #06B6D4"))
        except pyfiglet.FontNotFound:
            console.print("  [red]Fonte não disponível.[/red]")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Gerador de banner ASCII — Mission Control AI"
    )
    parser.add_argument("-fonts", action="store_true", help="Lista todas as fontes disponíveis")
    parser.add_argument("-font",  type=str, help="Testa uma fonte específica")
    parser.add_argument("-text",  type=str, default="Mission Control AI", help="Texto para testar")
    parser.add_argument("-demo",  action="store_true", help="Demonstra 8 fontes diferentes")
    args = parser.parse_args()

    if args.fonts:
        listar_fontes()
    elif args.demo:
        demonstrar_fontes()
    elif args.font:
        testar_fonte(args.font, args.text)
    else:
        exibir_banner_padrao()
