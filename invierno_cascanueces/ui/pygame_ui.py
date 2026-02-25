"""
ui/pygame_ui.py
───────────────
Bucle principal de Pygame.
Esta capa solo gestiona:
  - Ventana y reloj
  - Mover al soldado por el mapa
  - Partículas de nieve
  - Delegar render de sprites → ui.sprites
  - Delegar render de HUD    → ui.hud
  - Delegar lógica de juego  → engine.EstadoJuego
"""
import os
import sys
import random
import pygame

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from motor         import EstadoJuego, ACCIONES
from ui.sprites    import (TILE, build_castillo, build_arbol,
                            build_soldado_frame, build_mapa)
from ui.hud        import HUD

# ── Geometría de la ventana ───────────────────────────────────────────────────
COLS  = 20
ROWS  = 14
W     = COLS * TILE   # 640
MAP_H = ROWS * TILE   # 448
HUD_H = 120           # panel inferior
H     = MAP_H + HUD_H # 568
FPS   = 30

# ── Posiciones en el mapa (coordenadas de tile) ───────────────────────────────
POS = {
    "castillo"  : (6,  0),    # esquina superior izq del sprite (6×5 tiles)
    "arbol_a"   : (1,  4),    # árbol principal (frutos)
    "arbol_b"   : (16, 2),    # árbol derecho
    "arbol_c"   : (2,  9),    # árbol inferior
    "puerta"    : (9,  6),    # destino descansar / reparar
    "spawn"     : (10, 7),    # posición inicial del soldado
}

DESTINOS = {
    "recolectar": POS["arbol_a"],
    "descansar" : POS["puerta"],
    "reparar"   : POS["puerta"],
}

SPD = 2.5   # píxeles / frame


# ── Partícula de nieve ────────────────────────────────────────────────────────
class Copo:
    __slots__ = ("x", "y", "spd", "sz", "drift")

    def __init__(self, born=True):
        self.reset(born)

    def reset(self, born=True):
        self.x     = random.uniform(0, W)
        self.y     = random.uniform(-20, 0) if born else random.uniform(0, MAP_H)
        self.spd   = random.uniform(0.5, 1.5)
        self.sz    = random.choice([1, 1, 2])
        self.drift = random.uniform(-0.25, 0.25)

    def update(self):
        self.y += self.spd
        self.x += self.drift
        if self.y > MAP_H:
            self.reset()


# ── Entrada del log ───────────────────────────────────────────────────────────
class LogEntry:
    __slots__ = ("text", "color", "ttl")

    def __init__(self, text: str, color: tuple):
        self.text  = text
        self.color = color
        self.ttl   = FPS * 7   # 7 segundos de visibilidad


# ── Colores de log ────────────────────────────────────────────────────────────
LOG_COLORS = {
    "recolectar": (75, 225, 110),
    "descansar" : (120, 180, 255),
    "reparar"   : (50, 215, 85),
    "clima"     : (255, 95, 75),
    "arbol"     : (255, 200, 55),
}


# ── Clase principal ───────────────────────────────────────────────────────────
class PygameUI:

    def __init__(self):
        pygame.init()
        # Compatibilidad Python 3.13 / Windows — fallback sin SCALED
        try:
            self.window = pygame.display.set_mode(
                (W, H), pygame.SCALED | pygame.RESIZABLE, vsync=0)
        except Exception:
            self.window = pygame.display.set_mode((W, H))
        pygame.display.set_caption("El Invierno del Cascanueces")

        self.clock  = pygame.time.Clock()
        self.fonts  = self._load_fonts()
        self._reset()

    # ── Fuentes ───────────────────────────────────────────────────────────────

    def _load_fonts(self) -> dict:
        names = ["Courier New", "Consolas", "Lucida Console",
                 "DejaVu Sans Mono", "monospace"]
        def get(sz, bold=False):
            for n in names:
                try:
                    f = pygame.font.SysFont(n, sz, bold=bold)
                    if f:
                        return f
                except Exception:
                    pass
            return pygame.font.Font(None, sz)
        return {"s": get(13), "m": get(14, bold=True), "l": get(22, bold=True)}

    # ── Reset / inicio ────────────────────────────────────────────────────────

    def _reset(self):
        self.estado = EstadoJuego()
        self.log    : list[LogEntry] = []
        self.fase   = "esperando"   # "esperando"|"moviendose"|"clima"|"volviendo"
        self.accion_pendiente = None

        # Soldado
        sx = POS["spawn"][0] * TILE + TILE // 4
        sy = POS["spawn"][1] * TILE
        self.sol_x  = float(sx)
        self.sol_y  = float(sy)
        self.dest_x = self.sol_x
        self.dest_y = self.sol_y
        self.facing = "down"
        self.step   = 0
        self.step_t = 0

        # Sprites pre-renderizados
        self.mapa     = build_mapa(COLS, ROWS)
        self.cast_s   = build_castillo()
        self.arbol_f  = build_arbol(frutos=True)
        self.arbol_nf = build_arbol(frutos=False)
        # Cache de frames del soldado (facing × step) → 8 combos
        self.frames = {
            (f, st): build_soldado_frame(f, st)
            for f  in ("down", "up", "left", "right")
            for st in (0, 1)
        }

        # Partículas
        self.copos = [Copo(born=False) for _ in range(55)]

        # Storm overlay
        self.storm = pygame.Surface((W, MAP_H), pygame.SRCALPHA)
        self.storm.fill((8, 16, 58, 120))

        # HUD
        self.hud = HUD(W, MAP_H, HUD_H)

        # Fin
        self._blink = 0
        self._fin_ov = None  # surface de overlay de fin (se crea al detectar fin)

    # ── Bucle público ─────────────────────────────────────────────────────────

    def run(self):
        running = True
        while running:
            mouse = pygame.mouse.get_pos()
            self.hud.set_hover(mouse)

            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    running = False
                elif ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_ESCAPE:
                        running = False
                    else:
                        self._handle_key(ev.key)
                elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    self._handle_click(mouse)

            self._update()
            self._draw()
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

    # ── Eventos ───────────────────────────────────────────────────────────────

    def _handle_key(self, key):
        if self.estado.fin:
            self._reset()
            return
        km = {pygame.K_1: 0, pygame.K_2: 1, pygame.K_3: 2,
              pygame.K_KP1: 0, pygame.K_KP2: 1, pygame.K_KP3: 2}
        if key in km:
            self._iniciar_accion(ACCIONES[km[key]])

    def _handle_click(self, pos):
        if self.estado.fin:
            self._reset()
            return
        idx = self.hud.btn_at(pos)
        if idx >= 0:
            self._iniciar_accion(ACCIONES[idx])

    def _iniciar_accion(self, accion: str):
        if self.fase != "esperando" or self.estado.fin:
            return
        self.accion_pendiente = accion
        self.fase = "moviendose"
        dest = DESTINOS[accion]
        self._set_destino(dest[0] * TILE + TILE // 4,
                          dest[1] * TILE)
        self.hud.mark_dirty()

    # ── Update ────────────────────────────────────────────────────────────────

    def _update(self):
        if self.estado.fin:
            self._blink = (self._blink + 1) % (FPS * 2)
            return

        for c in self.copos:
            c.update()

        if self.fase == "moviendose":
            self.step_t += 1
            if self.step_t >= 6:
                self.step_t = 0
                self.step   = 1 - self.step

        if self.fase in ("moviendose", "volviendo"):
            self._mover_soldado()
            self.hud.mark_dirty()

    def _set_destino(self, dx: float, dy: float):
        self.dest_x = dx
        self.dest_y = dy
        ddx = dx - self.sol_x
        ddy = dy - self.sol_y
        if abs(ddx) >= abs(ddy):
            self.facing = "right" if ddx > 0 else "left"
        else:
            self.facing = "down" if ddy > 0 else "up"

    def _mover_soldado(self):
        dx   = self.dest_x - self.sol_x
        dy   = self.dest_y - self.sol_y
        dist = (dx * dx + dy * dy) ** 0.5
        if dist <= SPD + 0.5:
            self.sol_x = self.dest_x
            self.sol_y = self.dest_y
            self.step  = 0
            if self.fase == "moviendose":
                self._ejecutar_accion()
            else:
                self.fase = "esperando"
        else:
            f = SPD / dist
            self.sol_x += dx * f
            self.sol_y += dy * f

    def _ejecutar_accion(self):
        """Llama al engine y procesa los mensajes del resultado."""
        res = self.estado.ejecutar_turno(self.accion_pendiente)

        self._log(res["msg_accion"], LOG_COLORS[self.accion_pendiente])
        self._log(res["msg_clima"],  LOG_COLORS["clima"])
        if res["msg_arbol"]:
            self._log(res["msg_arbol"], LOG_COLORS["arbol"])

        self.accion_pendiente = None
        self.hud.mark_dirty()

        if self.estado.fin:
            self.fase = "esperando"
            self._build_fin_overlay()
        else:
            # Volver al spawn
            self.fase = "volviendo"
            self._set_destino(
                POS["spawn"][0] * TILE + TILE // 4,
                POS["spawn"][1] * TILE
            )

    def _log(self, text: str, color: tuple):
        self.log.insert(0, LogEntry(text, color))
        if len(self.log) > 5:
            self.log.pop()

    # ── Render ────────────────────────────────────────────────────────────────

    def _draw(self):
        w = self.window

        # Mapa base
        w.blit(self.mapa, (0, 0))

        # Castillo
        cx, cy = POS["castillo"]
        w.blit(self.cast_s, (cx * TILE, cy * TILE))

        # Árboles
        snap = self.estado.snapshot()
        for (tx, ty), es_principal in [
            (POS["arbol_a"], True),
            (POS["arbol_b"], False),
            (POS["arbol_c"], False),
        ]:
            has_f = es_principal and snap["arbol_frutos"] > 0
            w.blit(self.arbol_f if has_f else self.arbol_nf, (tx * TILE, ty * TILE))

        # Nieve
        for c in self.copos:
            self.window.fill((215, 232, 245), (int(c.x), int(c.y), c.sz, c.sz))

        # Overlay tormenta
        if self.fase == "clima":
            w.blit(self.storm, (0, 0))

        # Soldado
        frame = self.frames[(self.facing, self.step)]
        w.blit(frame, (int(self.sol_x), int(self.sol_y)))

        # HUD
        self.hud.draw(w, snap, self.log, self.fase, self.fonts)

        # Overlay fin
        if self.estado.fin and self._fin_ov:
            self._draw_fin()

    def _build_fin_overlay(self):
        ov = pygame.Surface((W, H), pygame.SRCALPHA)
        if self.estado.fin == "victoria":
            ov.fill((8, 32, 12, 185))
        else:
            ov.fill((32, 8, 8, 185))
        self._fin_ov = ov

    def _draw_fin(self):
        self.window.blit(self._fin_ov, (0, 0))

        fin = self.estado.fin
        if fin == "victoria":
            color = (80, 255, 120)
            l1    = "¡VICTORIA!"
            l2    = "Sobreviviste los 7 días de invierno."
        else:
            color = (255, 80, 60)
            l1    = "DERROTA"
            l2    = ("Los muros colapsaron."
                     if fin == "derrota_c"
                     else "El Cascanueces se congeló.")

        if self._blink < FPS:
            t1 = self.fonts["l"].render(l1, True, color)
            self.window.blit(t1, ((W - t1.get_width()) // 2, H // 2 - 44))

        t2 = self.fonts["m"].render(l2, True, (215, 230, 248))
        self.window.blit(t2, ((W - t2.get_width()) // 2, H // 2 + 4))

        t3 = self.fonts["s"].render(
            "Presiona cualquier tecla o haz click para reiniciar",
            True, (110, 135, 165))
        self.window.blit(t3, ((W - t3.get_width()) // 2, H // 2 + 28))


# ── Punto de entrada ─────────────────────────────────────────────────────────

def jugar_pygame():
    ui = PygameUI()
    ui.run()


if __name__ == "__main__":
    jugar_pygame()