"""
main.py — El Invierno del Cascanueces
──────────────────────────────────────
Punto de entrada único. Siempre arranca en la terminal con un menú
que pregunta cómo quiere jugar el usuario.

Uso directo (sin menú):
    python main.py --terminal   →  fuerza modo terminal
    python main.py --grafico    →  fuerza modo gráfico
"""

import os
import sys

# ── Asegurar que el directorio del proyecto esté primero en el path ───────────
# Esto garantiza que "motor", "ui" y "clases" se resuelvan desde aquí,
# y no desde algún paquete del sistema con el mismo nombre.
ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT != sys.path[0]:
    sys.path.insert(0, ROOT)

# ── ANSI helpers (funcionan en Windows 10+ con el venv activado) ──────────────
if os.name == "nt":
    os.system("color")   # habilita secuencias ANSI en Windows

RESET  = "\033[0m"
BOLD   = "\033[1m"
CYAN   = "\033[36m"
YELLOW = "\033[33m"
GREEN  = "\033[32m"
RED    = "\033[31m"
DIM    = "\033[2m"


# ── Menú de inicio ────────────────────────────────────────────────────────────

BANNER = f"""
{CYAN}{BOLD}╔══════════════════════════════════════════╗
║      EL INVIERNO DEL CASCANUECES        ║
╚══════════════════════════════════════════╝{RESET}

  Sobrevive {BOLD}7 días{RESET} de tormenta de invierno.
  Gestiona el castillo, la energía del soldado
  y los recursos del árbol mágico.

{YELLOW}  ¿Cómo quieres jugar?{RESET}

    {CYAN}{BOLD}1{RESET}  —  Terminal   {DIM}(solo texto, sin dependencias){RESET}
    {CYAN}{BOLD}2{RESET}  —  Gráfico    {DIM}(ventana Pygame, pixel-art){RESET}
    {CYAN}{BOLD}0{RESET}  —  Salir
"""


def menu_inicio() -> str:
    """
    Muestra el menú y devuelve 'terminal' | 'grafico' | 'salir'.
    """
    print(BANNER)
    while True:
        try:
            opcion = input(f"  {BOLD}Elige (0-2):{RESET} ").strip()
            if opcion == "1":
                return "terminal"
            if opcion == "2":
                return "grafico"
            if opcion == "0":
                return "salir"
            print(f"  {RED}Opción no válida. Escribe 0, 1 o 2.{RESET}")
        except (KeyboardInterrupt, EOFError):
            print()
            return "salir"


# ── Launchers ─────────────────────────────────────────────────────────────────

def lanzar_terminal():
    print(f"\n  {GREEN}Iniciando modo terminal...{RESET}\n")
    from ui.terminal import jugar_terminal
    jugar_terminal()


def lanzar_grafico():
    try:
        import pygame  # noqa: F401
    except ImportError:
        print(f"\n  {RED}Pygame no está instalado.{RESET}")
        print(f"  Instálalo con:  {BOLD}pip install pygame{RESET}")
        print(f"  O usa el modo terminal:  {BOLD}python main.py --terminal{RESET}\n")
        sys.exit(1)

    print(f"\n  {GREEN}Abriendo ventana Pygame...{RESET}\n")
    from ui.pygame_ui import jugar_pygame
    jugar_pygame()


# ── Punto de entrada ──────────────────────────────────────────────────────────

def main():
    args = [a.lower() for a in sys.argv[1:]]

    # Flags directos (saltan el menú)
    if "--terminal" in args or "-t" in args:
        lanzar_terminal()
        return
    if "--grafico" in args or "-g" in args:
        lanzar_grafico()
        return

    # Menú interactivo
    eleccion = menu_inicio()

    if eleccion == "terminal":
        lanzar_terminal()
    elif eleccion == "grafico":
        lanzar_grafico()
    else:
        print(f"\n  {DIM}¡Hasta la próxima!{RESET}\n")
        sys.exit(0)


if __name__ == "__main__":
    main()