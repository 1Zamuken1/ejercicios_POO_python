"""
ui/hud.py
─────────
Panel de interfaz de usuario (HUD) para la versión Pygame.
Dibuja barras de estado, log de eventos y botones de acción
sin solapamiento de texto.
"""
import pygame
from ui.sprites import TILE

# ── Paleta UI ─────────────────────────────────────────────────────────────────
UC = {
    "bg"         : ( 10,  14,  26),
    "bg_top"     : ( 18,  24,  44),
    "border"     : ( 48,  80, 140),
    "border_hi"  : ( 80, 130, 210),
    "text"       : (215, 230, 248),
    "dim"        : (110, 135, 165),
    "accent"     : (255, 205,  50),
    "accent2"    : ( 90, 195, 255),
    "bar_bg"     : ( 28,  36,  58),
    "bar_hi"     : ( 50, 215,  85),
    "bar_mid"    : (225, 205,  40),
    "bar_lo"     : (225,  55,  45),
    "bar_energy" : ( 60, 140, 255),
    "bar_tree"   : ( 45, 185,  80),
    "log_good"   : ( 75, 225, 110),
    "log_bad"    : (255,  95,  75),
    "log_warn"   : (255, 200,  55),
    "log_info"   : (120, 180, 255),
    "btn"        : ( 20,  46,  84),
    "btn_hover"  : ( 36,  78, 140),
    "btn_press"  : ( 14,  30,  60),
    "btn_border" : ( 55, 108, 185),
    "btn_border_hover": ( 90, 170, 255),
    "btn_text"   : (215, 232, 250),
    "btn_dim"    : (100, 130, 165),
    "white"      : (255, 255, 255),
    "outline"    : (  8,   8,  14),
}


def _hp_color(val: int, mx: int = 100) -> tuple:
    pct = val / max(1, mx)
    if pct <= 0.30:
        return UC["bar_lo"]
    if pct <= 0.60:
        return UC["bar_mid"]
    return UC["bar_hi"]


def draw_bar(surf, x, y, w, h, val, mx, base_color):
    """
    Barra con fondo, relleno y borde.
    Cambia de color (verde→amarillo→rojo) si se usa _hp_color como base.
    """
    pygame.draw.rect(surf, UC["bar_bg"],   (x, y, w, h))
    fill = max(0, int(w * val / max(1, mx)))
    if fill:
        pygame.draw.rect(surf, base_color, (x, y, fill, h))
    pygame.draw.rect(surf, UC["border"],   (x, y, w, h), 1)
    # Línea de peligro al 30%
    dx = x + int(w * 0.3)
    pygame.draw.line(surf, UC["bar_lo"], (dx, y + 1), (dx, y + h - 1), 1)


class HUD:
    """
    Renderiza el panel inferior del juego.
    Se crea una vez y se llama a draw() cada vez que el estado cambia.
    Usa una Surface interna con dirty flag para no repintar innecesariamente.
    """

    # Geometría del panel
    BTN_W  = 158
    BTN_H  = 36
    BTN_GAP = 12

    def __init__(self, screen_w: int, panel_y: int, panel_h: int):
        self.W  = screen_w
        self.Y  = panel_y       # coordenada Y absoluta en la ventana
        self.H  = panel_h

        self._surf  = pygame.Surface((screen_w, panel_h))
        self._dirty = True
        self._hover = -1

        # Pre-computar rects de botones (coordenadas absolutas de ventana)
        total_w = 3 * self.BTN_W + 2 * self.BTN_GAP
        start_x = (screen_w - total_w) // 2
        btn_y   = panel_y + panel_h - self.BTN_H - 10
        self.btn_rects = [
            pygame.Rect(start_x + i * (self.BTN_W + self.BTN_GAP),
                        btn_y, self.BTN_W, self.BTN_H)
            for i in range(3)
        ]
        # Etiquetas de botones (split en 2 líneas para evitar solapamiento)
        self.btn_labels = [
            ("1 — RECOLECTAR", "(+ener, árbol)"),
            ("2 — DESCANSAR",  "(+ener, −cast)"),
            ("3 — REPARAR",    "(−ener, +cast)"),
        ]

    # ── Público ───────────────────────────────────────────────────────────────

    def set_hover(self, mouse_pos: tuple) -> bool:
        """Actualiza el hover. Retorna True si cambió (para dirty flag)."""
        prev = self._hover
        self._hover = -1
        for i, r in enumerate(self.btn_rects):
            if r.collidepoint(mouse_pos):
                self._hover = i
        changed = self._hover != prev
        if changed:
            self._dirty = True
        return changed

    def mark_dirty(self):
        self._dirty = True

    def btn_at(self, mouse_pos: tuple) -> int:
        """Retorna el índice del botón clickeado, o -1."""
        for i, r in enumerate(self.btn_rects):
            if r.collidepoint(mouse_pos):
                return i
        return -1

    def draw(self, target: pygame.Surface, snap: dict,
             log: list, fase: str, fonts: dict):
        """
        Dibuja el HUD sobre `target`.
        snap  → dict del EstadoJuego.snapshot()
        log   → lista de LogEntry
        fase  → "esperando" | "moviendose" | "clima" | "volviendo"
        fonts → {"s": font_small, "m": font_medium, "l": font_large}
        """
        if not self._dirty:
            target.blit(self._surf, (0, self.Y))
            return

        s = self._surf
        s.fill(UC["bg"])

        # Franja superior del panel
        pygame.draw.rect(s, UC["bg_top"], (0, 0, self.W, 44))
        pygame.draw.line(s, UC["border_hi"], (0, 0),  (self.W, 0),  2)
        pygame.draw.line(s, UC["border"],    (0, 44), (self.W, 44), 1)

        fs = fonts["s"]
        fm = fonts["m"]

        # ── DÍA ──────────────────────────────────────────────────────────────
        day_txt = fm.render(
            f"DÍA  {snap['dia']} / {snap['dias_max']}", True, UC["accent"]
        )
        s.blit(day_txt, (self.W - day_txt.get_width() - 16, 10))

        # ── BARRAS DE ESTADO ─────────────────────────────────────────────────
        bar_defs = [
            ("CASTILLO", snap["castillo_hp"],       100, _hp_color(snap["castillo_hp"])),
            ("ENERGÍA",  snap["soldado_energia"],   100, UC["bar_energy"]),
            ("ÁRBOL-R",  snap["arbol_resistencia"], 100, UC["bar_tree"]),
        ]
        bar_w  = 115
        col_w  = 160
        bar_h  = 10

        for i, (label, val, mx, col) in enumerate(bar_defs):
            bx = 12 + i * col_w
            # Etiqueta
            lt = fs.render(label, True, UC["dim"])
            s.blit(lt, (bx, 6))
            # Barra
            draw_bar(s, bx, 22, bar_w, bar_h, max(0, val), mx, col)
            # Valor numérico a la derecha de la barra
            vt = fs.render(f"{max(0, val):>3}", True, col)
            s.blit(vt, (bx + bar_w + 4, 20))

        # Frutos (columna extra)
        fr_col = UC["log_good"] if snap["arbol_frutos"] >= 5 else (
                 UC["log_warn"] if snap["arbol_frutos"] > 0 else UC["log_bad"])
        fr_lbl = fs.render("FRUTOS", True, UC["dim"])
        fr_val = fs.render(f"{snap['arbol_frutos']:>3}", True, fr_col)
        bx_fr  = 12 + 3 * col_w
        s.blit(fr_lbl, (bx_fr, 6))
        s.blit(fr_val, (bx_fr, 20))

        # ── LOG DE EVENTOS ───────────────────────────────────────────────────
        # Zona entre barras y botones: y=48 hasta btn_y
        btn_y_local = self.btn_rects[0].y - self.Y
        log_start   = 48
        log_h       = btn_y_local - log_start - 4
        n_lines     = min(3, log_h // 16)

        for i, entry in enumerate(log[:n_lines]):
            if entry.ttl > 0:
                entry.ttl -= 1
                alpha = min(255, entry.ttl * 8)
                lt = fs.render(f"> {entry.text[:72]}", True, entry.color)
                lt.set_alpha(alpha)
                s.blit(lt, (12, log_start + i * 16))

        # ── INDICADOR DE FASE (esquina inferior derecha) ─────────────────────
        fase_msgs = {
            "moviendose": ("Moviéndose...",        UC["accent2"]),
            "clima"     : ("Tormenta!",          UC["log_bad"]),
            "volviendo" : ("Volviendo al castillo...", UC["log_warn"]),
        }
        if fase in fase_msgs and fase != "esperando":
            txt, col = fase_msgs[fase]
            ft = fm.render(txt, True, col)
            s.blit(ft, (self.W - ft.get_width() - 12,
                        btn_y_local - ft.get_height() - 4))

        # ── BOTONES ──────────────────────────────────────────────────────────
        enabled = (fase == "esperando")

        for i, (top_lbl, sub_lbl) in enumerate(self.btn_labels):
            rabs = self.btn_rects[i]
            rl   = pygame.Rect(rabs.x, rabs.y - self.Y, rabs.w, rabs.h)

            if not enabled:
                bg, brd, tc, sc = (UC["btn_press"], UC["border"],
                                   UC["btn_dim"],   UC["btn_dim"])
            elif self._hover == i:
                bg, brd, tc, sc = (UC["btn_hover"],  UC["btn_border_hover"],
                                   UC["white"],       UC["accent2"])
            else:
                bg, brd, tc, sc = (UC["btn"],        UC["btn_border"],
                                   UC["btn_text"],    UC["btn_dim"])

            pygame.draw.rect(s, bg,  rl, border_radius=5)
            pygame.draw.rect(s, brd, rl, 1, border_radius=5)

            # Línea separadora interna
            sep_y = rl.y + rl.h - 14
            pygame.draw.line(s, brd, (rl.x + 6, sep_y), (rl.x + rl.w - 6, sep_y), 1)

            # Texto principal (centrado verticalmente en la parte superior)
            lt = fm.render(top_lbl, True, tc)
            lx = rl.x + (rl.w - lt.get_width())  // 2
            ly = rl.y + (rl.h - 14 - lt.get_height()) // 2
            s.blit(lt, (lx, ly))

            # Subtexto (en la franja inferior del botón, bajo la línea sep)
            st = fs.render(sub_lbl, True, sc)
            sx = rl.x + (rl.w - st.get_width()) // 2
            sy = sep_y + 2
            s.blit(st, (sx, sy))

        self._dirty = False
        target.blit(self._surf, (0, self.Y))