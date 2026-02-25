"""
motor/estado.py
───────────────
Núcleo del juego: estado, turnos y lógica de victoria/derrota.
NO depende de Pygame — puede ser usado tanto por la UI gráfica
como por la interfaz de terminal.
"""
import os
import sys
import random

# Asegurar que el root del proyecto esté en el path
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from clases.castillo import Castillo
from clases.soldado  import Soldado
from clases.arbol    import Arbol

# ─────────────────────────────────────────────────────
# Estadísticas iniciales (balanceadas para tensión real)
# ─────────────────────────────────────────────────────
CONFIG = {
    "castillo_hp"       : 70,
    "soldado_energia"   : 65,
    "arbol_frutos"      : 10,
    "arbol_resistencia" : 80,
    "danio_min"         :  8,
    "danio_max"         : 18,
    "dias_max"          :  7,
}

ACCIONES = ("recolectar", "descansar", "reparar")


class EstadoJuego:
    """
    Encapsula todo el estado mutable del juego.
    Las UIs (terminal o Pygame) solo llaman a:
        - estado.ejecutar_turno(accion)   → dict con mensajes del turno
        - estado.fin                      → None | "victoria" | "derrota_c" | "derrota_s"
        - estado.snapshot()               → dict con valores actuales para render
    """

    def __init__(self):
        self.castillo  = Castillo("Fortaleza del Norte",
                                   integridad_inicial=CONFIG["castillo_hp"])
        self.soldado   = Soldado("Cascanueces",
                                  energia_inicial=CONFIG["soldado_energia"])
        self.arbol     = Arbol("Pino Mágico",
                                frutos_iniciales=CONFIG["arbol_frutos"],
                                resistencia_frio=CONFIG["arbol_resistencia"])
        self.dia       = 1
        self.dias_max  = CONFIG["dias_max"]
        self.fin       = None          # None | "victoria" | "derrota_c" | "derrota_s"
        self._historial: list[dict] = []

    # ── API pública ──────────────────────────────────────────────────────────

    def ejecutar_turno(self, accion: str) -> dict:
        """
        Ejecuta la acción del jugador y el turno del clima.
        Devuelve un dict con los mensajes generados.
        Modifica self.fin si el juego terminó.
        """
        assert accion in ACCIONES, f"Acción inválida: {accion}"
        assert self.fin is None,   "El juego ya terminó."

        resultado = {
            "dia"        : self.dia,
            "accion"     : accion,
            "msg_accion" : "",
            "danio"      : 0,
            "msg_clima"  : "",
            "msg_arbol"  : "",
        }

        # 1. Acción del jugador
        if accion == "recolectar":
            resultado["msg_accion"] = self.soldado.recolectar_frutos(self.arbol)
        elif accion == "descansar":
            resultado["msg_accion"] = self.castillo.refugiar_soldado(self.soldado)
        elif accion == "reparar":
            resultado["msg_accion"] = self.castillo.reparar(self.soldado)

        # 2. Turno del clima
        danio = random.randint(CONFIG["danio_min"], CONFIG["danio_max"])
        resultado["danio"]     = danio
        resultado["msg_clima"] = self.castillo.recibir_danio_clima(danio)
        self.arbol.sufrir_frio(danio // 2)
        resultado["msg_arbol"] = self.arbol.regenerar() or ""

        # 3. Avanzar día
        self.dia += 1
        self._historial.append(resultado)

        # 4. Verificar fin de partida
        if self.castillo.integridad <= 0:
            self.fin = "derrota_c"
        elif self.soldado.energia <= 0:
            self.fin = "derrota_s"
        elif self.dia > self.dias_max:
            self.fin = "victoria"

        return resultado

    def snapshot(self) -> dict:
        """Estado actual para que las UIs puedan renderizar."""
        return {
            "dia"              : self.dia,
            "dias_max"         : self.dias_max,
            "castillo_hp"      : self.castillo.integridad,
            "soldado_energia"  : self.soldado.energia,
            "arbol_resistencia": self.arbol.resistencia_frio,
            "arbol_frutos"     : self.arbol.frutos,
            "fin"              : self.fin,
        }

    def historial(self) -> list[dict]:
        return list(self._historial)