import pygame
import random
import sys

try:
    import cardgame
    HAS_CARDGAME = True
except ImportError:
    HAS_CARDGAME = False

try:
    import deck_viewer as deck_manager
    HAS_DECK_MANAGER = True
except ImportError:
    HAS_DECK_MANAGER = False

# =====================
# Screen
# =====================
WIDTH, HEIGHT = 1920, 1080

# =====================
# Palette
# =====================
BG            = (12,  14,  20)
PANEL         = (20,  24,  34)
PANEL2        = (26,  30,  42)
BORDER        = (38,  46,  64)
CARD_BG       = (30,  36,  50)
CARD_HOV      = (44,  54,  76)
CARD_BORD     = (50,  62,  88)
CARD_BORD_ACT = (80, 160, 220)
WHITE         = (225, 232, 245)
MUTED         = (95,  108, 132)
DIM           = (55,  65,  85)
RED           = (210,  65,  65)
AMBER         = (215, 155,  45)
BLUE          = (75,  145, 255)
TEAL          = (45,  195, 165)
GREEN         = (65,  190,  95)
PURPLE        = (145,  90, 220)

CATEGORY_COLORS = {
    "All":     BLUE,
    "Core":    TEAL,
    "Toon":    PURPLE,
    "Special": AMBER,
    "Exodia":  RED,
    "Units":   (75,  175, 120),
    "Spells":  (180, 100, 220),
    "AA":      (220, 140,  60),
}

# =====================
# Layout
# =====================
PAD        = 14
SIDEBAR_X  = 1490
SIDEBAR_W  = WIDTH - SIDEBAR_X + 8
CARD_W     = 150
CARD_H     = 150
CARD_GAP   = 10
CARD_CW    = CARD_W + CARD_GAP
CARD_CH    = CARD_H + CARD_GAP
COLS       = 9
STATUS_DUR = 180

GRID_X = PAD
GRID_Y = 60
GRID_W = SIDEBAR_X - GRID_X - PAD
GRID_H = HEIGHT - GRID_Y - 60

import cards
CARD_CATALOG = cards.ALL_CARDS
CATEGORIES   = ["All", "Core", "Toon", "Special", "Exodia", "Units", "Spells", "AA"]

SORT_MODES   = ["Default", "A→Z", "Z→A", "Value ↑", "Value ↓"]


# =====================
# Helpers
# =====================
def rrect(surf, color, rect, r=8, bw=0, bc=None):
    pygame.draw.rect(surf, color, rect, border_radius=r)
    if bw and bc:
        pygame.draw.rect(surf, bc, rect, bw, border_radius=r)

def panel(surf, rect, r=10):
    rrect(surf, PANEL, rect, r)
    rrect(surf, BORDER, rect, r, 1)

def clamp(val, lo, hi):
    return max(lo, min(hi, val))

def wrap_text(font, text, max_w):
    words, lines, line = text.split(), [], ""
    for w in words:
        test = (line + " " + w).strip()
        if font.size(test)[0] <= max_w:
            line = test
        else:
            if line: lines.append(line)
            line = w
    if line: lines.append(line)
    return lines

def draw_value_orb(surf, value, cx, cy, accent, font, orb_r=18):
    """Draw a concentric-ring orb with numeric value centred inside."""
    pygame.draw.circle(surf, accent,  (cx, cy), orb_r)
    pygame.draw.circle(surf, PANEL2,  (cx, cy), orb_r - 3)
    pygame.draw.circle(surf, accent,  (cx, cy), orb_r - 7)
    vs = font.render(str(value), True, WHITE)
    surf.blit(vs, (cx - vs.get_width() // 2, cy - vs.get_height() // 2))


# =====================
# Image cache
# =====================
_img_cache = {}

def load_image(path, w, h):
    key = (path, w, h)
    if key in _img_cache:
        return _img_cache[key]
    try:
        img = pygame.image.load(path).convert_alpha()
        img = pygame.transform.smoothscale(img, (w, h))
    except Exception:
        img = pygame.Surface((w, h), pygame.SRCALPHA)
        img.fill((40, 40, 60, 200))
    _img_cache[key] = img
    return img


# =====================
# Scrollable grid
# =====================
class CardGrid:
    def __init__(self, display, clip_rect, cols=COLS):
        self.display     = display
        self.clip_rect   = clip_rect
        self.cols        = cols
        self.scroll_y    = 0
        self._max_scroll = 0

    def scroll(self, dy):
        self.scroll_y = clamp(self.scroll_y + dy, 0, max(0, self._max_scroll))

    def reset_scroll(self): self.scroll_y = 0

    def card_pos(self, idx):
        col = idx % self.cols
        row = idx // self.cols
        return (self.clip_rect.x + col * CARD_CW,
                self.clip_rect.y + row * CARD_CH - self.scroll_y)

    def update_max_scroll(self, count):
        rows = max(1, (count + self.cols - 1) // self.cols)
        self._max_scroll = max(0, rows * CARD_CH - self.clip_rect.height)

    def card_at(self, pos, count):
        if not self.clip_rect.collidepoint(pos): return None
        for i in range(count):
            x, y = self.card_pos(i)
            if x <= pos[0] <= x + CARD_W and y <= pos[1] <= y + CARD_H:
                return i
        return None

    def draw_clip_start(self): self.display.set_clip(self.clip_rect)
    def draw_clip_end(self):   self.display.set_clip(None)


# =====================
# Card Viewer
# =====================
class CardViewer:
    def __init__(self, display):
        self.display = display

        self.fonts = {
            "normal": pygame.font.Font(None, 24),
            "small":  pygame.font.Font(None, 20),
            "large":  pygame.font.Font(None, 40),
            "title":  pygame.font.Font(None, 32),
            "xlarge": pygame.font.Font(None, 52),
            "desc":   pygame.font.Font(None, 22),
            "tiny":   pygame.font.Font(None, 17),
        }

        self.all_cards     = list(CARD_CATALOG)
        self.active_cat    = "All"
        self.sort_mode     = "Default"
        self.filtered      = list(self.all_cards)
        self.selected_card = None

        self.status        = ""
        self.status_timer  = 0

        self.sidebar_scroll_y    = 0
        self._sidebar_max_scroll = 0

        grid_clip = pygame.Rect(GRID_X, GRID_Y + 50, GRID_W, GRID_H - 50)
        self.grid = CardGrid(display, grid_clip, cols=COLS)

        self._build_cat_tabs()
        self._build_sort_tabs()

    # ------------------------------------------------------------------
    def _build_cat_tabs(self):
        tw, th, tg = 110, 34, 6
        self.cat_tabs = {
            cat: pygame.Rect(GRID_X + i * (tw + tg), GRID_Y + 8, tw, th)
            for i, cat in enumerate(CATEGORIES)
        }

    def _build_sort_tabs(self):
        tw, th, tg = 90, 24, 5
        # Place sort tabs to the right of category tabs, aligned top-right of grid
        start_x = SIDEBAR_X - len(SORT_MODES) * (tw + tg) - PAD
        self.sort_tabs = {
            m: pygame.Rect(start_x + i * (tw + tg), GRID_Y + 16, tw, th)
            for i, m in enumerate(SORT_MODES)
        }

    def _apply_filter_sort(self):
        base = (self.all_cards if self.active_cat == "All"
                else [c for c in self.all_cards if c["category"] == self.active_cat])
        if self.sort_mode == "A→Z":
            base = sorted(base, key=lambda c: c["name"])
        elif self.sort_mode == "Z→A":
            base = sorted(base, key=lambda c: c["name"], reverse=True)
        elif self.sort_mode == "Value ↑":
            base = sorted(base, key=lambda c: c.get("value", 0))
        elif self.sort_mode == "Value ↓":
            base = sorted(base, key=lambda c: c.get("value", 0), reverse=True)
        self.filtered = base
        self.grid.reset_scroll()

    def set_category(self, cat):
        self.active_cat = cat
        self._apply_filter_sort()
        self.set_status(f"{cat}  ·  {len(self.filtered)} cards")

    def set_sort(self, mode):
        self.sort_mode = mode
        self._apply_filter_sort()
        self.set_status(f"Sorted: {mode}")

    def pick_random(self):
        if self.filtered:
            self.selected_card = random.choice(self.filtered)
            self.sidebar_scroll_y = 0
            self.set_status(f"Random: {self.selected_card['name']}")

    def set_status(self, msg):
        self.status       = msg
        self.status_timer = STATUS_DUR

    def tick_status(self):
        if self.status_timer > 0:
            self.status_timer -= 1
            if self.status_timer == 0:
                self.status = ""

    # =====================
    # Events
    # =====================
    def handle_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return False

            elif e.type == pygame.MOUSEWHEEL:
                mx, my = pygame.mouse.get_pos()
                sb = pygame.Rect(SIDEBAR_X - 8, 0, SIDEBAR_W, HEIGHT)
                if sb.collidepoint(mx, my):
                    self.sidebar_scroll_y = clamp(
                        self.sidebar_scroll_y - e.y * 25,
                        0, max(0, self._sidebar_max_scroll)
                    )
                elif self.grid.clip_rect.collidepoint(mx, my):
                    self.grid.scroll(-e.y * 30)

            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                pos = e.pos
                # Category tabs
                for cat, rect in self.cat_tabs.items():
                    if rect.collidepoint(pos):
                        self.set_category(cat); break
                else:
                    # Sort tabs
                    for mode, rect in self.sort_tabs.items():
                        if rect.collidepoint(pos):
                            self.set_sort(mode); break
                    else:
                        idx = self.grid.card_at(pos, len(self.filtered))
                        if idx is not None:
                            self.selected_card    = self.filtered[idx]
                            self.sidebar_scroll_y = 0
                            self.set_status(f"Viewing: {self.selected_card['name']}")

            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    if HAS_CARDGAME: cardgame.main()
                    return False
                elif e.key == pygame.K_d:
                    if HAS_DECK_MANAGER: deck_manager.main()
                    return False
                elif e.key == pygame.K_r:
                    self.selected_card = None
                    self.set_category("All")
                    self.sort_mode = "Default"
                    self.set_status("Reset")
                elif e.key == pygame.K_x:
                    self.pick_random()
                elif e.key == pygame.K_LEFT:
                    cats = CATEGORIES
                    self.set_category(cats[(cats.index(self.active_cat) - 1) % len(cats)])
                elif e.key == pygame.K_RIGHT:
                    cats = CATEGORIES
                    self.set_category(cats[(cats.index(self.active_cat) + 1) % len(cats)])
                elif e.key == pygame.K_f:
                    # Cycle sort modes
                    idx = SORT_MODES.index(self.sort_mode)
                    self.set_sort(SORT_MODES[(idx + 1) % len(SORT_MODES)])
                for ki, cat in enumerate(CATEGORIES[1:], 1):
                    if e.key == getattr(pygame, f"K_{ki}", None):
                        self.set_category(cat)

        return True

    # =====================
    # Drawing helpers
    # =====================
    def _txt(self, text, x, y, color=WHITE, fk="normal"):
        s = self.fonts[fk].render(text, True, color)
        self.display.blit(s, (x, y))
        return s

    def draw_scrollbar(self):
        r          = self.grid.clip_rect
        count      = len(self.filtered)
        total_rows = max(1, (count + COLS - 1) // COLS)
        vis_rows   = r.height / CARD_CH
        if total_rows <= vis_rows: return
        track   = pygame.Rect(r.right + 4, r.top, 5, r.height)
        rrect(self.display, PANEL2, track, r=2)
        ratio   = vis_rows / total_rows
        thumb_h = max(20, int(r.height * ratio))
        frac    = self.grid.scroll_y / max(1, self.grid._max_scroll)
        thumb_y = r.top + int((r.height - thumb_h) * frac)
        rrect(self.display, TEAL, pygame.Rect(r.right + 4, thumb_y, 5, thumb_h), r=2)

    def draw_category_tabs(self):
        for cat, rect in self.cat_tabs.items():
            active  = (cat == self.active_cat)
            col     = CATEGORY_COLORS.get(cat, BLUE)
            bg      = (28, 40, 60) if active else PANEL
            bord    = col if active else BORDER
            rrect(self.display, bg, rect, r=7)
            rrect(self.display, bord, rect, r=7, bw=2 if active else 1)
            s = self.fonts["small"].render(cat, True, WHITE if active else MUTED)
            self.display.blit(s, (rect.centerx - s.get_width() // 2,
                                  rect.centery - s.get_height() // 2))

    def draw_sort_tabs(self):
        for mode, rect in self.sort_tabs.items():
            active = (mode == self.sort_mode)
            col    = AMBER if active else BORDER
            bg     = (38, 34, 18) if active else PANEL
            rrect(self.display, bg, rect, r=5)
            rrect(self.display, col, rect, r=5, bw=1)
            s = self.fonts["tiny"].render(mode, True, AMBER if active else MUTED)
            self.display.blit(s, (rect.centerx - s.get_width() // 2,
                                  rect.centery - s.get_height() // 2))

    def draw_card_tile(self, card, pos, hovered=False):
        rx, ry  = pos
        bg      = CARD_HOV if hovered else CARD_BG
        bord    = CARD_BORD_ACT if hovered else CARD_BORD
        r       = pygame.Rect(rx, ry, CARD_W, CARD_H)
        rrect(self.display, bg, r, r=7)
        rrect(self.display, bord, r, r=7, bw=1)

        cat_col = CATEGORY_COLORS.get(card["category"], BLUE)
        stripe  = pygame.Rect(rx + 1, ry + 1, CARD_W - 2, 4)
        pygame.draw.rect(self.display, cat_col, stripe,
                         border_top_left_radius=6, border_top_right_radius=6)

        img = load_image(card["image"], CARD_W - 4, CARD_H - 24)
        self.display.blit(img, (rx + 2, ry + 6))

        # Value orb — bottom-left corner of tile
        value = card.get("value", None)
        if value is not None:
            draw_value_orb(self.display, value,
                           rx + 14, ry + CARD_H - 14,
                           cat_col, self.fonts["tiny"], orb_r=11)

        # Name label
        ns = self.fonts["small"].render(card["name"], True, WHITE)
        if ns.get_width() > CARD_W - 28:
            ns = self.fonts["tiny"].render(card["name"], True, WHITE)
        self.display.blit(ns, (rx + CARD_W // 2 - ns.get_width() // 2 + 6,
                               ry + CARD_H - 16))

        # Selected ring
        if self.selected_card and self.selected_card["name"] == card["name"]:
            rrect(self.display, TEAL, r, r=7, bw=2, bc=TEAL)

    def draw_grid(self):
        count = len(self.filtered)
        self.grid.update_max_scroll(count)

        panel_r = pygame.Rect(GRID_X - PAD, GRID_Y - 4,
                              GRID_W + PAD + 18, GRID_H + 60)
        panel(self.display, panel_r, r=10)

        lx, ly = GRID_X, GRID_Y - PAD + 56 + 14
        col = CATEGORY_COLORS.get(self.active_cat, BLUE)
        self._txt(self.active_cat.upper(), lx, ly - 36, col, "small")
        self._txt(f"{count} cards", lx + 60, ly - 36, MUTED, "small")
        if self.sort_mode != "Default":
            self._txt(f"↕ {self.sort_mode}", lx + 130, ly - 36, AMBER, "small")
        if self.grid._max_scroll > 0:
            self._txt("scroll ↕", panel_r.right - 72, ly - 36, DIM, "small")

        mx, my = pygame.mouse.get_pos()
        self.grid.draw_clip_start()
        for i, card in enumerate(self.filtered):
            pos = self.grid.card_pos(i)
            cr  = self.grid.clip_rect
            if cr.top - CARD_H <= pos[1] <= cr.bottom:
                hov = (pos[0] <= mx <= pos[0] + CARD_W and
                       pos[1] <= my <= pos[1] + CARD_H and
                       cr.collidepoint(mx, my))
                self.draw_card_tile(card, pos, hovered=hov)
        self.grid.draw_clip_end()
        self.draw_scrollbar()

    def draw_sidebar(self):
        sx = SIDEBAR_X
        panel(self.display, pygame.Rect(sx - 8, 0, SIDEBAR_W, HEIGHT), r=0)
        self.display.set_clip(pygame.Rect(sx - 8, 0, SIDEBAR_W, HEIGHT))
        oy = -self.sidebar_scroll_y

        self._txt("Card Viewer", sx + 6, 18 + oy, WHITE, "title")
        cat_col = CATEGORY_COLORS.get(self.active_cat, BLUE)
        self._txt(self.active_cat, sx + 6, 54 + oy, cat_col, "normal")
        pygame.draw.line(self.display, BORDER, (sx, 80 + oy), (WIDTH - 4, 80 + oy), 1)

        cy = 94 + oy
        pw = SIDEBAR_W - 28   # preview width

        # ── Card preview ──────────────────────────────────────────────
        card = self.selected_card
        if card is not None:
            cat_col_p = CATEGORY_COLORS.get(card["category"], BLUE)

            # Accent bar
            pygame.draw.rect(self.display, cat_col_p,
                             pygame.Rect(sx + 6, cy, pw, 6),
                             border_top_left_radius=8, border_top_right_radius=8)

            # Image
            iw = pw - 8
            ih = int(iw * 1.0)
            img = load_image(card["image"], iw, ih)
            self.display.blit(img, (sx + 10, cy + 8))
            cy += ih + 14

            # Name
            ns = self.fonts["large"].render(card["name"], True, WHITE)
            if ns.get_width() > pw - 8:
                ns = self.fonts["normal"].render(card["name"], True, WHITE)
            self.display.blit(ns, (sx + 6 + pw // 2 - ns.get_width() // 2, cy))
            cy += ns.get_height() + 4

            # Category badge
            cat_s = self.fonts["small"].render(card["category"].upper(), True, cat_col_p)
            self.display.blit(cat_s, (sx + 6 + pw // 2 - cat_s.get_width() // 2, cy))
            cy += cat_s.get_height() + 8

            # Value orb
            value = card.get("value", None)
            if value is not None:
                orb_r  = 20
                orb_cx = sx + 6 + pw // 2
                orb_cy = cy + orb_r
                draw_value_orb(self.display, value, orb_cx, orb_cy,
                               cat_col_p, self.fonts["normal"], orb_r)
                cy += orb_r * 2 + 10

            # Description
            desc = card.get("desc", "")
            if desc:
                pygame.draw.line(self.display, BORDER,
                                 (sx + 12, cy), (sx + 6 + pw - 6, cy), 1)
                cy += 8
                for line in wrap_text(self.fonts["desc"], desc, pw - 16):
                    ds = self.fonts["desc"].render(line, True, MUTED)
                    self.display.blit(ds, (sx + 14, cy))
                    cy += ds.get_height() + 2
                cy += 4

            pygame.draw.line(self.display, BORDER, (sx, cy + 4), (WIDTH - 4, cy + 4), 1)
            cy += 12
        else:
            hint_r = pygame.Rect(sx + 6, cy, pw, 60)
            rrect(self.display, PANEL2, hint_r, r=8)
            t = self.fonts["small"].render("Click a card to preview", True, MUTED)
            self.display.blit(t, (hint_r.centerx - t.get_width() // 2,
                                  hint_r.centery - t.get_height() // 2))
            cy += 72

        # ── Controls ──────────────────────────────────────────────────
        controls = [
            ("ESC",  "Main menu"),
            ("D",    "Deck Manager"),
            ("R",    "Reset / All"),
            ("X",    "Random card"),
            ("F",    "Cycle sort"),
            ("←/→",  "Switch category"),
            ("1–7",  "Jump to category"),
        ]
        for key, desc in controls:
            if cy + 28 > HEIGHT + self.sidebar_scroll_y - 10: break
            kr = pygame.Rect(sx + 6, cy, 34, 20)
            rrect(self.display, (32, 44, 62), kr, r=4)
            ks = self.fonts["small"].render(key, True, BLUE)
            self.display.blit(ks, (kr.centerx - ks.get_width() // 2, kr.y + 2))
            self._txt(desc, sx + 46, cy + 2, MUTED, "small")
            cy += 28

        pygame.draw.line(self.display, BORDER, (sx, cy + 2), (WIDTH - 4, cy + 2), 1)
        cy += 10

        # ── Category list ─────────────────────────────────────────────
        self._txt("Categories", sx + 6, cy, WHITE, "small"); cy += 20
        for cat in CATEGORIES[1:]:
            count = sum(1 for c in self.all_cards if c["category"] == cat)
            col   = CATEGORY_COLORS.get(cat, BLUE)
            dot   = pygame.Rect(sx + 10, cy + 4, 8, 8)
            rrect(self.display, col, dot, r=4)
            active = (cat == self.active_cat)
            self._txt(cat,        sx + 24,  cy, WHITE if active else MUTED, "small")
            self._txt(str(count), sx + 110, cy, DIM,   "small")
            cy += 20

        pygame.draw.line(self.display, BORDER, (sx, cy + 4), (WIDTH - 4, cy + 4), 1)
        cy += 12

        # ── Sort indicator ────────────────────────────────────────────
        self._txt("Sort", sx + 6, cy, WHITE, "small"); cy += 20
        for mode in SORT_MODES:
            active = (mode == self.sort_mode)
            col = AMBER if active else MUTED
            prefix = "● " if active else "  "
            self._txt(prefix + mode, sx + 10, cy, col, "small")
            cy += 18
        cy += 4

        pygame.draw.line(self.display, BORDER, (sx, cy + 4), (WIDTH - 4, cy + 4), 1)
        cy += 12

        # ── Stats ─────────────────────────────────────────────────────
        self._txt("Stats", sx + 6, cy, WHITE, "small"); cy += 20
        self._txt(f"Total    {len(self.all_cards)}", sx + 6, cy, MUTED, "small"); cy += 20
        self._txt(f"Showing  {len(self.filtered)}",  sx + 6, cy, MUTED, "small"); cy += 20

        pygame.draw.line(self.display, BORDER, (sx, cy + 4), (WIDTH - 4, cy + 4), 1)
        cy += 12

        # ── Status ───────────────────────────────────────────────────
        if self.status:
            col = (GREEN if any(w in self.status for w in ("Viewing","Reset","Loaded","Random","Sorted"))
                   else RED if any(w in self.status for w in ("error","No"))
                   else TEAL)
            self._txt(self.status, sx + 6, cy, col, "normal")
            cy += 28

        # Sidebar scroll book-keeping
        content_bottom = cy + self.sidebar_scroll_y
        self._sidebar_max_scroll = max(0, content_bottom - HEIGHT + 20)
        self.display.set_clip(None)

        # Sidebar scrollbar
        if self._sidebar_max_scroll > 0:
            track = pygame.Rect(WIDTH - 6, 0, 4, HEIGHT)
            rrect(self.display, PANEL2, track, r=2)
            ratio   = HEIGHT / max(1, content_bottom)
            thumb_h = max(20, int(HEIGHT * ratio))
            frac    = self.sidebar_scroll_y / max(1, self._sidebar_max_scroll)
            thumb_y = int((HEIGHT - thumb_h) * frac)
            rrect(self.display, TEAL, pygame.Rect(WIDTH - 6, thumb_y, 4, thumb_h), r=2)

    def draw_header(self):
        bar = pygame.Rect(0, 0, WIDTH, 52)
        rrect(self.display, PANEL, bar, r=0)
        pygame.draw.line(self.display, BORDER, (0, 52), (WIDTH, 52), 1)
        self._txt("✦  Card Viewer", 20, 14, WHITE, "title")
        hint = self.fonts["small"].render(
            "← → categories  ·  F sort  ·  X random  ·  click to preview", True, DIM
        )
        self.display.blit(hint, (WIDTH // 2 - hint.get_width() // 2, 18))

    def draw(self):
        self.tick_status()
        self.display.fill(BG)
        self.draw_header()
        self.draw_category_tabs()
        self.draw_sort_tabs()
        self.draw_grid()
        self.draw_sidebar()


# =====================
# Main
# =====================
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Card Viewer")
    clock  = pygame.time.Clock()
    viewer = CardViewer(screen)
    viewer.set_status(f"All  ·  {len(CARD_CATALOG)} cards loaded")

    running = True
    while running:
        running = viewer.handle_events()
        viewer.draw()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()