"""
ui/sprites.py
─────────────
Sprites pixel-art estilo Social Empires:
  - Outlines negros en todos los objetos
  - Colores saturados y contrastados
  - Sombras bajo los objetos
  - Todo generado con pygame.draw (cero assets externos)
"""
import pygame

# ── Constantes de tamaño ──────────────────────────────────────────────────────
TILE = 32   # unidad base en píxeles

# ── Paleta Social Empires ─────────────────────────────────────────────────────
C = {
    # Suelo
    "snow"        : (215, 232, 245),
    "snow_alt"    : (200, 218, 235),
    "snow_shadow" : (170, 196, 218),
    "path"        : (170, 138, 100),
    "path_dark"   : (135, 108,  76),
    "path_edge"   : ( 90,  70,  48),
    # Castillo — piedra gris azulada con detalles cálidos
    "stone"       : ( 96,  96, 108),
    "stone_hi"    : (130, 132, 148),
    "stone_sh"    : ( 60,  60,  70),
    "merlon"      : ( 72,  72,  84),
    "tower_top"   : ( 52,  52,  62),
    "door_bg"     : ( 24,  18,  12),
    "door_arch"   : ( 48,  38,  26),
    "window_warm" : (255, 228, 120),
    "window_cool" : (180, 210, 240),
    "flag_red"    : (210,  40,  40),
    "flag_pole"   : (180, 140,  80),
    # Árbol de pino
    "trunk"       : (120,  76,  36),
    "trunk_sh"    : ( 80,  48,  18),
    "pine_a"      : ( 36, 140,  56),   # capa inferior (la más oscura)
    "pine_b"      : ( 52, 180,  72),   # capa media
    "pine_c"      : ( 72, 220,  96),   # capa superior (la más clara)
    "pine_snow"   : (230, 245, 255),
    "fruit"       : (230,  48,  36),
    "fruit_hi"    : (255, 100,  80),
    # Soldado cascanueces
    "body_coat"   : (180,  36,  36),   # Casaca roja
    "body_coat_sh": (130,  22,  22),
    "pants"       : ( 28,  50, 110),   # Pantalón azul marino
    "pants_sh"    : ( 18,  34,  80),
    "boots"       : ( 40,  28,  14),
    "skin"        : (240, 200, 158),
    "skin_sh"     : (200, 158, 110),
    "hair"        : ( 80,  50,  20),
    "hat_body"    : ( 36,  36,  80),   # Gorro azul oscuro
    "hat_brim"    : ( 24,  24,  58),
    "hat_trim"    : (220, 180,  60),   # Galón dorado
    "scarf"       : (240, 200,  40),   # Bufanda amarilla
    "sword"       : (200, 210, 220),
    "sword_grip"  : (180, 130,  40),
    # Misc
    "outline"     : (  8,   8,  12),
    "shadow"      : (  0,   0,   0),
    "shadow_alpha": 45,
}


def _outline(surf: pygame.Surface, color=None):
    """
    Dibuja un outline de 1px alrededor de todos los píxeles opacos de
    la surface SRCALPHA. Muy ligero para sprites pequeños.
    """
    col = color or C["outline"]
    w, h = surf.get_size()
    out  = pygame.Surface((w, h), pygame.SRCALPHA)
    for dx, dy in ((-1,0),(1,0),(0,-1),(0,1)):
        out.blit(surf, (dx, dy))
    # Colorear el outline
    mask = pygame.mask.from_surface(surf)
    outline_surf = mask.to_surface(setcolor=col + (255,), unsetcolor=(0,0,0,0))
    result = pygame.Surface((w, h), pygame.SRCALPHA)
    result.blit(outline_surf, (0, 0))
    result.blit(surf, (0, 0))
    return result


def _r(s, color, x, y, w, h):
    """Rellena un rect de color sólido."""
    s.fill(color, (x, y, w, h))


def _shadow_ellipse(target: pygame.Surface, cx: int, cy: int, rw: int, rh: int):
    """Dibuja una elipse de sombra semi-transparente en la surface destino."""
    sh = pygame.Surface((rw * 2, rh * 2), pygame.SRCALPHA)
    pygame.draw.ellipse(sh, (0, 0, 0, C["shadow_alpha"]), (0, 0, rw * 2, rh * 2))
    target.blit(sh, (cx - rw, cy - rh))


# ─────────────────────────────────────────────────────────────────────────────
# CASTILLO  — 6×5 tiles (192×160 px)
# Estilo Social Empires: torre central alta, 2 torres laterales más bajas,
# almenas pronunciadas, bandera, ventanas cálidas, puerta con arco apuntado.
# ─────────────────────────────────────────────────────────────────────────────
def build_castillo() -> pygame.Surface:
    CW, CH = 6 * TILE, 5 * TILE          # 192 × 160
    s = pygame.Surface((CW, CH), pygame.SRCALPHA)

    T = TILE
    # ── Torres laterales (2T × 3T) ──
    for tx in (0, 4 * T):
        # Cuerpo
        pygame.draw.rect(s, C["stone"],    (tx,          T,     2*T,    3*T))
        pygame.draw.rect(s, C["stone_hi"], (tx,          T,     4,      3*T))
        pygame.draw.rect(s, C["stone_sh"], (tx + 2*T-4,  T,     4,      3*T))
        # Techo plano + almenas
        pygame.draw.rect(s, C["merlon"],   (tx,          T,     2*T,    T//3))
        for i in range(4):
            if i % 2 == 0:
                pygame.draw.rect(s, C["tower_top"], (tx + i * (T//2), T - T//3, T//2 - 2, T//3))
        # Ventana
        wx, wy = tx + T//2 - 4, T + T//2
        pygame.draw.rect(s, C["outline"],     (wx-1, wy-1, 10, 12))
        pygame.draw.rect(s, C["window_warm"], (wx,   wy,   8,  10))
        # Cruz de ventana
        pygame.draw.line(s, C["stone_sh"], (wx+4, wy), (wx+4, wy+10), 1)
        pygame.draw.line(s, C["stone_sh"], (wx, wy+5), (wx+8, wy+5),  1)

    # ── Muralla central (2T × 2T, entre las torres) ──
    pygame.draw.rect(s, C["stone"],    (2*T,       2*T,   2*T,   2*T))
    pygame.draw.rect(s, C["stone_hi"], (2*T,       2*T,   3,     2*T))
    pygame.draw.rect(s, C["stone_sh"], (4*T - 3,   2*T,   3,     2*T))

    # ── Torre central (2T × 4T, la más alta) ──
    pygame.draw.rect(s, C["stone"],    (2*T,         0,     2*T,   3*T))
    pygame.draw.rect(s, C["stone_hi"], (2*T,         0,     5,     3*T))
    pygame.draw.rect(s, C["stone_sh"], (4*T - 5,     0,     5,     3*T))
    # Techo + almenas torre central
    pygame.draw.rect(s, C["merlon"],   (2*T,         0,     2*T,   T//3))
    for i in range(5):
        if i % 2 == 0:
            pygame.draw.rect(s, C["tower_top"],
                             (2*T + i * (T//2 - 1) - 2, -T//3, T//2 - 2, T//3 + 2))
    # Ventana grande torre central
    wx2, wy2 = 2*T + T//2 - 5, T//2
    pygame.draw.rect(s, C["outline"],     (wx2-1, wy2-1, 12, 14))
    pygame.draw.rect(s, C["window_warm"], (wx2,   wy2,   10, 12))
    pygame.draw.line(s, C["stone_sh"], (wx2+5, wy2), (wx2+5, wy2+12), 1)
    pygame.draw.line(s, C["stone_sh"], (wx2, wy2+6), (wx2+10, wy2+6), 1)

    # Bandera en torre central
    pygame.draw.line(s, C["flag_pole"], (2*T + T, -T//3 - 2), (2*T + T, -T//3 - 12), 2)
    pts_flag = [(2*T+T+2, -T//3-12), (2*T+T+2, -T//3-6), (2*T+T+10, -T//3-9)]
    pygame.draw.polygon(s, C["flag_red"], pts_flag)

    # ── Sillería (líneas de mortero) ──
    for row in range(0, CH, T//2):
        pygame.draw.line(s, C["stone_sh"], (0, row), (CW, row), 1)
    for col_x in range(0, CW, T//2):
        pygame.draw.line(s, C["stone_sh"], (col_x, 0), (col_x, CH), 1)

    # ── Puerta con arco apuntado ──
    door_x, door_w, door_h = 2*T + T//4, T + T//2, T + T//3
    door_y = CH - door_h
    pygame.draw.rect(s, C["door_arch"], (door_x - 3, door_y - 3, door_w + 6, door_h + 3))
    pygame.draw.rect(s, C["door_bg"],   (door_x,     door_y,     door_w,     door_h))
    # Arco apuntado (2 arcos de medio punto)
    arc_r = door_w // 2
    pygame.draw.arc(s, C["door_bg"],
                    (door_x, door_y - arc_r, arc_r, arc_r * 2),
                    0, 3.14159, arc_r)
    pygame.draw.arc(s, C["door_bg"],
                    (door_x + arc_r, door_y - arc_r, arc_r, arc_r * 2),
                    0, 3.14159, arc_r)

    return s


# ─────────────────────────────────────────────────────────────────────────────
# ÁRBOL DE PINO  — 3×4 tiles con outline
# ─────────────────────────────────────────────────────────────────────────────
def build_arbol(frutos: bool) -> pygame.Surface:
    TW, TH = 3 * TILE, 4 * TILE
    s = pygame.Surface((TW, TH), pygame.SRCALPHA)
    cx = TW // 2

    # Sombra
    _shadow_ellipse(s, cx, TH - 4, 24, 8)

    # Tronco
    pygame.draw.rect(s, C["trunk_sh"], (cx - 5, TH - TILE + 2,  10, TILE - 4))
    pygame.draw.rect(s, C["trunk"],    (cx - 4, TH - TILE + 2,   6, TILE - 4))

    # Copa en 3 capas triangulares (de abajo a arriba, cada vez más pequeña y clara)
    layers = [
        (TH - TILE - 10,  TW - 8,   C["pine_a"],  22),
        (TH - TILE - 30,  TW - 24,  C["pine_b"],  22),
        (TH - TILE - 48,  TW - 40,  C["pine_c"],  18),
    ]
    for top_y, width, color, layer_h in layers:
        pts = [
            (cx,               top_y),
            (cx - width // 2,  top_y + layer_h),
            (cx + width // 2,  top_y + layer_h),
        ]
        pygame.draw.polygon(s, color, pts)
        # Highlight borde izquierdo (luz)
        brighter = tuple(min(255, v + 30) for v in color)
        pygame.draw.line(s, brighter, pts[0], pts[1], 1)

    # Nieve en las copas
    pygame.draw.ellipse(s, C["pine_snow"],
                        (cx - 14, TH - TILE - 26, 28, 10))
    pygame.draw.ellipse(s, C["pine_snow"],
                        (cx - 9,  TH - TILE - 44, 18, 8))
    pygame.draw.ellipse(s, C["pine_snow"],
                        (cx - 5,  TH - TILE - 58, 10, 6))

    # Frutos
    if frutos:
        for fx, fy in [
            (cx - 10, TH - TILE - 14), (cx + 6,  TH - TILE - 12),
            (cx - 5,  TH - TILE - 22), (cx + 10, TH - TILE - 20),
            (cx + 2,  TH - TILE - 8),
        ]:
            pygame.draw.circle(s, C["outline"], (fx, fy), 4)
            pygame.draw.circle(s, C["fruit"],   (fx, fy), 3)
            pygame.draw.circle(s, C["fruit_hi"],(fx - 1, fy - 1), 1)

    return _outline(s)


# ─────────────────────────────────────────────────────────────────────────────
# SOLDADO CASCANUECES  — ~14×22 px lógicos dentro de un tile
# Estilo Social Empires: casaca roja, pantalón azul, gorro con galón dorado,
# bufanda amarilla, espada al costado.
# ─────────────────────────────────────────────────────────────────────────────
def build_soldado_frame(facing: str = "down", step: int = 0) -> pygame.Surface:
    """
    Devuelve un sprite de 24×30 px SRCALPHA.
    facing: "down" | "up" | "left" | "right"
    step:   0 | 1  (frame de animación de piernas)
    """
    SW, SH = 24, 30
    s = pygame.Surface((SW, SH), pygame.SRCALPHA)

    # Piernas (animadas)
    l_off = 2 if step == 1 else 0
    # Bota izquierda
    pygame.draw.rect(s, C["pants"],    ( 5, 18 + l_off,  5, 6))
    pygame.draw.rect(s, C["boots"],    ( 5, 24 + l_off,  5, 4))
    # Bota derecha
    pygame.draw.rect(s, C["pants"],    (13, 18 - l_off,  5, 6))
    pygame.draw.rect(s, C["boots"],    (13, 24 - l_off,  5, 4))

    # Casaca (cuerpo)
    pygame.draw.rect(s, C["body_coat"],    ( 4, 10, 15, 10))
    pygame.draw.rect(s, C["body_coat_sh"], ( 4, 10,  3, 10))   # sombra lateral

    # Botones dorados
    for by in (12, 15, 18):
        pygame.draw.rect(s, C["hat_trim"], (10, by, 2, 2))

    # Bufanda
    pygame.draw.rect(s, C["scarf"], (4, 14, 15, 3))

    # Espada (costado derecho)
    pygame.draw.rect(s, C["sword_grip"], (19, 12, 3, 5))
    pygame.draw.rect(s, C["sword"],      (20,  4, 2, 9))

    # Cabeza
    pygame.draw.rect(s, C["skin_sh"], (6,  5, 11, 7))
    pygame.draw.rect(s, C["skin"],    (7,  4, 10, 7))

    # Ojos (solo si no está mirando hacia arriba)
    if facing != "up":
        pygame.draw.rect(s, C["outline"], (8,  6, 2, 2))
        pygame.draw.rect(s, C["outline"], (13, 6, 2, 2))
        # Brillo ojo
        pygame.draw.rect(s, (255, 255, 255), (8,  6, 1, 1))
        pygame.draw.rect(s, (255, 255, 255), (13, 6, 1, 1))

    # Cabello (si mira hacia arriba)
    if facing == "up":
        pygame.draw.rect(s, C["hair"], (7, 4, 10, 4))

    # Gorro
    pygame.draw.rect(s, C["hat_brim"], ( 5, 3, 13, 3))    # ala
    pygame.draw.rect(s, C["hat_body"], ( 7, -3, 9, 7))    # cuerpo del gorro
    pygame.draw.rect(s, C["hat_trim"], ( 5, 3, 13, 2))    # galón dorado

    return _outline(s)


# ─────────────────────────────────────────────────────────────────────────────
# MAPA BASE — precalculado una sola vez
# ─────────────────────────────────────────────────────────────────────────────
def build_mapa(cols: int, rows: int) -> pygame.Surface:
    """
    Suelo de nieve + caminos con bordes suaves.
    Variación de tile determinista (no random) para patrón estable.
    """
    W = cols * TILE
    H = rows * TILE
    s = pygame.Surface((W, H))

    # Suelo de nieve con variación de 2 tonos (patrón diagonales sutiles)
    for ty in range(rows):
        for tx in range(cols):
            # Variación con hash determinista — ni checker agresivo ni ruido
            val = (tx * 2 + ty * 3) % 7
            color = C["snow_alt"] if val == 0 else C["snow"]
            s.fill(color, (tx * TILE, ty * TILE, TILE, TILE))

    # Camino vertical central (ancho 3 tiles: 9,10,11)
    road_x = 9 * TILE
    road_w = 3 * TILE
    s.fill(C["path"],      (road_x,              0, road_w, H))
    s.fill(C["path_dark"], (road_x,              0, 5,      H))       # borde izq
    s.fill(C["path_dark"], (road_x + road_w - 5, 0, 5,      H))       # borde der
    s.fill(C["path_edge"], (road_x,              0, 2,      H))       # línea izq
    s.fill(C["path_edge"], (road_x + road_w - 2, 0, 2,      H))       # línea der

    # Camino horizontal izquierdo (fila 6 → árbol izq)
    hy = 6 * TILE
    s.fill(C["path"],      (0,      hy,          road_x, TILE))
    s.fill(C["path_dark"], (0,      hy,          road_x, 4))
    s.fill(C["path_dark"], (0,      hy + TILE-4, road_x, 4))
    s.fill(C["path_edge"], (0,      hy,          road_x, 2))
    s.fill(C["path_edge"], (0,      hy + TILE-2, road_x, 2))

    # Camino horizontal derecho (fila 4 → árbol der)
    hy2    = 4 * TILE
    right_x = road_x + road_w
    s.fill(C["path"],      (right_x, hy2,          W - right_x, TILE))
    s.fill(C["path_dark"], (right_x, hy2,          W - right_x, 4))
    s.fill(C["path_dark"], (right_x, hy2 + TILE-4, W - right_x, 4))

    return s