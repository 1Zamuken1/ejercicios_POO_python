"""
ui/terminal.py
──────────────
Interfaz de texto para jugar en la terminal.
Usa ANSI colors para resaltar el estado (funciona en Windows 10+,
PowerShell y cualquier terminal moderna).
No depende de Pygame en absoluto.
"""
import os
import sys

# Asegurar que el root del proyecto esté en el path
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from motor import EstadoJuego, ACCIONES

# ── ANSI helpers ─────────────────────────────────────────────────────────────
def _ansi(code): return f"\033[{code}m"
RESET  = _ansi(0)
BOLD   = _ansi(1)
RED    = _ansi(31)
GREEN  = _ansi(32)
YELLOW = _ansi(33)
BLUE   = _ansi(34)
CYAN   = _ansi(36)
WHITE  = _ansi(37)
DIM    = _ansi(2)

def color_hp(val, mx=100):
    pct = val / max(1, mx)
    if pct <= 0.3:  return RED
    if pct <= 0.6:  return YELLOW
    return GREEN

def barra(val, mx=100, ancho=20):
    pct   = max(0, min(1, val / max(1, mx)))
    lleno = int(ancho * pct)
    vacio = ancho - lleno
    col   = color_hp(val, mx)
    return f"{col}{'█' * lleno}{DIM}{'░' * vacio}{RESET}"

def limpiar():
    os.system("cls" if os.name == "nt" else "clear")

# ── Pantalla principal ────────────────────────────────────────────────────────

def mostrar_estado(snap: dict):
    limpiar()
    print(f"\n{BOLD}{CYAN}{'═'*50}{RESET}")
    print(f"  {BOLD}EL INVIERNO DEL CASCANUECES{RESET}")
    print(f"{BOLD}{CYAN}{'═'*50}{RESET}")
    print(f"  {BOLD}DÍA {snap['dia']} / {snap['dias_max']}{RESET}\n")

    # Barras de estado
    rows = [
        ("Castillo  ", snap["castillo_hp"],       100),
        ("Energía   ", snap["soldado_energia"],    100),
        ("Árbol-R   ", snap["arbol_resistencia"],  100),
    ]
    for label, val, mx in rows:
        col = color_hp(val, mx)
        print(f"  {WHITE}{label}{RESET} {barra(val, mx)}  "
              f"{col}{BOLD}{val:>3}{RESET}/{mx}")

    frutos_col = GREEN if snap["arbol_frutos"] >= 5 else (YELLOW if snap["arbol_frutos"] > 0 else RED)
    print(f"\n  {WHITE}Frutos disponibles:{RESET}  "
          f"{frutos_col}{BOLD}{snap['arbol_frutos']}{RESET}\n")

def mostrar_menu():
    print(f"  {BOLD}¿Qué orden le darás al soldado?{RESET}")
    print(f"  {CYAN}1{RESET}. Recolectar frutos  "
          f"{DIM}(+energía del árbol, cuesta energía de viaje){RESET}")
    print(f"  {CYAN}2{RESET}. Descansar          "
          f"{DIM}(+25 energía, −10 integridad del castillo){RESET}")
    print(f"  {CYAN}3{RESET}. Reparar muros      "
          f"{DIM}(+20 integridad, −15 energía){RESET}")
    print()

def mostrar_resultado(res: dict):
    print(f"\n{BOLD}{'─'*50}{RESET}")
    print(f"  {BOLD}> ACCIÓN:{RESET}  {GREEN}{res['msg_accion']}{RESET}")
    print(f"  {BOLD}CLIMA:{RESET}  {RED}{res['msg_clima']}{RESET}")
    if res["msg_arbol"]:
        col = YELLOW if "débil" in res["msg_arbol"] else GREEN
        print(f"  {BOLD}ÁRBOL:{RESET}  {col}{res['msg_arbol']}{RESET}")
    print(f"{BOLD}{'─'*50}{RESET}\n")
    input(f"  {DIM}[Presiona Enter para continuar...]{RESET}")

def mostrar_fin(fin: str):
    limpiar()
    print(f"\n{BOLD}{CYAN}{'═'*50}{RESET}")
    if fin == "victoria":
        print(f"\n  {BOLD}{GREEN}¡VICTORIA!{RESET}")
        print(f"  Sobreviviste los 7 días de invierno.")
    elif fin == "derrota_c":
        print(f"\n  {BOLD}{RED}DERROTA{RESET}")
        print(f"  Los muros del castillo colapsaron.")
    else:
        print(f"\n  {BOLD}{RED}DERROTA{RESET}")
        print(f"  El Cascanueces se congeló sin energía.")
    print(f"\n{BOLD}{CYAN}{'═'*50}{RESET}\n")

def pedir_accion() -> str:
    """Solicita una opción válida al usuario."""
    while True:
        try:
            opcion = int(input(f"  {BOLD}Elige (1-3):{RESET} ").strip())
            if 1 <= opcion <= 3:
                return ACCIONES[opcion - 1]
            print(f"  {RED}Opción no válida. Elige 1, 2 o 3.{RESET}")
        except (ValueError, KeyboardInterrupt):
            print(f"\n  {DIM}Saliendo...{RESET}")
            sys.exit(0)

# ── Bucle principal terminal ──────────────────────────────────────────────────

def jugar_terminal():
    """Punto de entrada para la modalidad terminal."""
    # Habilitar ANSI en Windows
    if os.name == "nt":
        os.system("color")

    estado = EstadoJuego()

    while estado.fin is None:
        mostrar_estado(estado.snapshot())
        mostrar_menu()
        accion    = pedir_accion()
        resultado = estado.ejecutar_turno(accion)
        mostrar_resultado(resultado)

    mostrar_fin(estado.fin)

    otra = input("  ¿Jugar otra vez? (s/n): ").strip().lower()
    if otra == "s":
        jugar_terminal()


if __name__ == "__main__":
    jugar_terminal()