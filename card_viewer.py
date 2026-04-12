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
BORDER_HI     = (60,  80, 120)
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

GRID_X      = PAD
GRID_Y      = 60       # top of the panel
GRID_W      = SIDEBAR_X - GRID_X - PAD
GRID_H      = HEIGHT - GRID_Y - 60
HEADER_H    = 34       # height of the in-panel label/pill row
GRID_CLIP_Y = GRID_Y + HEADER_H + 8   # where cards start

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

    def ensure_visible(self, idx):
        """Scroll so that card at idx is fully visible."""
        row      = idx // self.cols
        card_top = row * CARD_CH
        card_bot = card_top + CARD_H
        vis_top  = self.scroll_y
        vis_bot  = vis_top + self.clip_rect.height
        if card_top < vis_top:
            self.scroll_y = clamp(card_top, 0, self._max_scroll)
        elif card_bot > vis_bot:
            self.scroll_y = clamp(card_bot - self.clip_rect.height, 0, self._max_scroll)

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
        self.cursor_idx    = -1   # -1 = no keyboard cursor active

        self.status        = ""
        self.status_timer  = 0

        self.sidebar_scroll_y    = 0
        self._sidebar_max_scroll = 0

        # Nav mode: "mouse" or "keys" — keys mode shows cursor ring
        self._nav_mode = "mouse"

        grid_clip = pygame.Rect(GRID_X, GRID_CLIP_Y, GRID_W,
                               HEIGHT - GRID_CLIP_Y - 20)
        self.grid = CardGrid(display, grid_clip, cols=COLS)

        # Pill rects built each frame in _build_pill_rects()
        self._cat_pill_rects  = {}
        self._sort_pill_rects = {}

    # ------------------------------------------------------------------
    def _build_pill_rects(self):
        fn  = self.fonts["tiny"]
        ph  = 20
        gap = 5
        py  = GRID_Y + (HEADER_H - ph) // 2 + 2

        px = GRID_X
        self._cat_pill_rects = {}
        for cat in CATEGORIES:
            pw = max(32, fn.size(cat)[0] + 14)
            self._cat_pill_rects[cat] = pygame.Rect(px, py, pw, ph)
            px += pw + gap

        # Sort pills — right-aligned
        total_sw = sum(max(32, fn.size(m)[0] + 10) for m in SORT_MODES)
        total_sw += 4 * (len(SORT_MODES) - 1)
        sx = GRID_X + GRID_W - total_sw - 18
        self._sort_pill_rects = {}
        for mode in SORT_MODES:
            pw = max(32, fn.size(mode)[0] + 10)
            self._sort_pill_rects[mode] = pygame.Rect(sx, py, pw, ph)
            sx += pw + 4

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
        self.filtered  = base
        self.cursor_idx = -1
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
            idx = random.randrange(len(self.filtered))
            self._set_cursor(idx)
            self.sidebar_scroll_y = 0
            self.set_status(f"Random: {self.filtered[idx]['name']}")

    def _set_cursor(self, idx):
        """Set keyboard cursor and selected card, auto-scroll grid."""
        if not self.filtered:
            return
        idx = clamp(idx, 0, len(self.filtered) - 1)
        self.cursor_idx    = idx
        self.selected_card = self.filtered[idx]
        self.sidebar_scroll_y = 0
        self.grid.update_max_scroll(len(self.filtered))
        self.grid.ensure_visible(idx)

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

            elif e.type == pygame.MOUSEMOTION:
                # Switch to mouse mode on any movement
                self._nav_mode = "mouse"

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
                for cat, rect in self._cat_pill_rects.items():
                    if rect.collidepoint(pos):
                        self.set_category(cat); break
                else:
                    for mode, rect in self._sort_pill_rects.items():
                        if rect.collidepoint(pos):
                            self.set_sort(mode); break
                    else:
                        idx = self.grid.card_at(pos, len(self.filtered))
                        if idx is not None:
                            self._nav_mode = "mouse"
                            self.cursor_idx    = idx
                            self.selected_card = self.filtered[idx]
                            self.sidebar_scroll_y = 0
                            self.set_status(f"Viewing: {self.selected_card['name']}")

            elif e.type == pygame.KEYDOWN:
                self._handle_keydown(e)

        return True

    def _handle_keydown(self, e):
        # ── Navigation keys switch to key mode ──────────────────────
        arrow_keys = (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN)

        if e.key in arrow_keys:
            self._nav_mode = "keys"
            self._arrow_navigate(e.key)
            return

        if e.key == pygame.K_RETURN or e.key == pygame.K_SPACE:
            # Confirm selection at cursor
            if self.cursor_idx >= 0 and self.filtered:
                self.selected_card    = self.filtered[self.cursor_idx]
                self.sidebar_scroll_y = 0
                self.set_status(f"Viewing: {self.selected_card['name']}")
            return

        if e.key == pygame.K_HOME:
            self._nav_mode = "keys"
            self._set_cursor(0)
            self.set_status("First card")
            return

        if e.key == pygame.K_END:
            self._nav_mode = "keys"
            self._set_cursor(len(self.filtered) - 1)
            self.set_status("Last card")
            return

        if e.key == pygame.K_PAGEDOWN:
            self._nav_mode = "keys"
            step = COLS * max(1, self.grid.clip_rect.height // CARD_CH)
            self._set_cursor(self.cursor_idx + step)
            return

        if e.key == pygame.K_PAGEUP:
            self._nav_mode = "keys"
            step = COLS * max(1, self.grid.clip_rect.height // CARD_CH)
            self._set_cursor(self.cursor_idx - step)
            return

        if e.key == pygame.K_ESCAPE:
            if HAS_CARDGAME: cardgame.main()
            return

        if e.key == pygame.K_d:
            if HAS_DECK_MANAGER: deck_manager.main()
            return

        if e.key == pygame.K_r:
            self.selected_card = None
            self.cursor_idx    = -1
            self._nav_mode     = "mouse"
            self.set_category("All")
            self.sort_mode = "Default"
            self.set_status("Reset")
            return

        if e.key == pygame.K_x:
            self._nav_mode = "keys"
            self.pick_random()
            return

        if e.key == pygame.K_f:
            idx = SORT_MODES.index(self.sort_mode)
            self.set_sort(SORT_MODES[(idx + 1) % len(SORT_MODES)])
            return

        if e.key == pygame.K_TAB:
            # Cycle categories forward (shift+tab = backward)
            mods = pygame.key.get_mods()
            cats = CATEGORIES
            idx  = cats.index(self.active_cat)
            if mods & pygame.KMOD_SHIFT:
                self.set_category(cats[(idx - 1) % len(cats)])
            else:
                self.set_category(cats[(idx + 1) % len(cats)])
            return

        # Left/right for category switching (only when NOT in keys nav mode)
        if self._nav_mode == "mouse":
            if e.key == pygame.K_LEFT:
                cats = CATEGORIES
                self.set_category(cats[(cats.index(self.active_cat) - 1) % len(cats)])
                return
            if e.key == pygame.K_RIGHT:
                cats = CATEGORIES
                self.set_category(cats[(cats.index(self.active_cat) + 1) % len(cats)])
                return

        # Number keys: jump to category
        for ki, cat in enumerate(CATEGORIES[1:], 1):
            if e.key == getattr(pygame, f"K_{ki}", None):
                self.set_category(cat)
                return

    def _arrow_navigate(self, key):
        """Move keyboard cursor through the grid."""
        if not self.filtered:
            return

        count = len(self.filtered)
        cols  = COLS

        # If no cursor yet, start at 0
        if self.cursor_idx < 0:
            self._set_cursor(0)
            self.set_status(f"{self.filtered[0]['name']}")
            return

        idx = self.cursor_idx

        if key == pygame.K_RIGHT:
            idx = min(idx + 1, count - 1)
        elif key == pygame.K_LEFT:
            idx = max(idx - 1, 0)
        elif key == pygame.K_DOWN:
            idx = min(idx + cols, count - 1)
        elif key == pygame.K_UP:
            idx = max(idx - cols, 0)

        if idx != self.cursor_idx:
            self._set_cursor(idx)
            self.set_status(f"{self.filtered[idx]['name']}")

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

    def draw_pills(self):
        """Draw category pills and sort pills inside the panel header row."""
        fn  = self.fonts["tiny"]
        mx, my = pygame.mouse.get_pos()

        # ── Category pills ────────────────────────────────────────────
        for cat, rect in self._cat_pill_rects.items():
            active  = (cat == self.active_cat)
            col     = CATEGORY_COLORS.get(cat, BLUE)
            hov     = rect.collidepoint(mx, my) and not active
            bg      = (28, 40, 62) if active else ((32, 40, 56) if hov else PANEL2)
            bord    = col if active else (BORDER_HI if hov else BORDER)
            rrect(self.display, bg, rect, r=5)
            rrect(self.display, bord, rect, r=5, bw=2 if active else 1)
            tc = WHITE if active else (MUTED if not hov else (col[0]//2+128, col[1]//2+128, col[2]//2+128))
            s = fn.render(cat, True, tc)
            self.display.blit(s, (rect.centerx - s.get_width() // 2,
                                  rect.centery - s.get_height() // 2))
            # small count dot on active pill
            if active:
                cnt_s = pygame.font.Font(None, 14).render(str(len(self.filtered)), True, col)
                self.display.blit(cnt_s, (rect.right - cnt_s.get_width() - 2, rect.top + 1))

        # ── Sort pills ────────────────────────────────────────────────
        for mode, rect in self._sort_pill_rects.items():
            active = (mode == self.sort_mode)
            hov    = rect.collidepoint(mx, my) and not active
            bg     = (40, 36, 18) if active else ((32, 30, 18) if hov else PANEL2)
            bord   = AMBER if active else (BORDER_HI if hov else BORDER)
            rrect(self.display, bg, rect, r=5)
            rrect(self.display, bord, rect, r=5, bw=2 if active else 1)
            tc = AMBER if active else (MUTED if not hov else (200, 170, 90))
            s = fn.render(mode, True, tc)
            self.display.blit(s, (rect.centerx - s.get_width() // 2,
                                  rect.centery - s.get_height() // 2))

    def draw_card_tile(self, card, idx, pos, hovered=False):
        rx, ry  = pos
        is_cursor   = (self._nav_mode == "keys" and idx == self.cursor_idx)
        is_selected = (self.selected_card and self.selected_card["name"] == card["name"])

        if is_cursor:
            bg, bord = CARD_HOV, CARD_BORD_ACT
        elif hovered:
            bg, bord = CARD_HOV, CARD_BORD_ACT
        else:
            bg, bord = CARD_BG, CARD_BORD

        r = pygame.Rect(rx, ry, CARD_W, CARD_H)
        rrect(self.display, bg, r, r=7)
        rrect(self.display, bord, r, r=7, bw=1)

        cat_col = CATEGORY_COLORS.get(card["category"], BLUE)
        stripe  = pygame.Rect(rx + 1, ry + 1, CARD_W - 2, 4)
        pygame.draw.rect(self.display, cat_col, stripe,
                         border_top_left_radius=6, border_top_right_radius=6)

        img = load_image(card["image"], CARD_W - 4, CARD_H - 24)
        self.display.blit(img, (rx + 2, ry + 6))

        value = card.get("value", None)
        if value is not None:
            draw_value_orb(self.display, value,
                           rx + 14, ry + CARD_H - 14,
                           cat_col, self.fonts["tiny"], orb_r=11)

        ns = self.fonts["small"].render(card["name"], True, WHITE)
        if ns.get_width() > CARD_W - 28:
            ns = self.fonts["tiny"].render(card["name"], True, WHITE)
        self.display.blit(ns, (rx + CARD_W // 2 - ns.get_width() // 2 + 6,
                               ry + CARD_H - 16))

        # Selection ring (teal = selected/confirmed, white pulse = cursor)
        if is_selected and is_cursor:
            rrect(self.display, TEAL, r, r=7, bw=3, bc=TEAL)
        elif is_selected:
            rrect(self.display, TEAL, r, r=7, bw=2, bc=TEAL)
        elif is_cursor:
            # Animated pulse: brightness oscillates
            t   = pygame.time.get_ticks()
            alpha = int(160 + 80 * abs((t % 800) / 400 - 1))
            pulse_col = (min(255, BLUE[0] + 40), min(255, BLUE[1] + 40), min(255, BLUE[2] + 40))
            rrect(self.display, pulse_col, r, r=7, bw=2, bc=pulse_col)

            # Small arrow indicator above cursor card (only in key mode)
            ax, ay = rx + CARD_W // 2, ry - 6
            pygame.draw.polygon(self.display, BLUE,
                                [(ax, ay + 6), (ax - 6, ay), (ax + 6, ay)])

    def draw_grid(self):
        count = len(self.filtered)
        self.grid.update_max_scroll(count)

        # Outer panel (full area)
        panel_r = pygame.Rect(GRID_X - PAD, GRID_Y - 4,
                              GRID_W + PAD + 18, HEIGHT - GRID_Y + 4)
        panel(self.display, panel_r, r=10)

        # Header row background
        hdr_r = pygame.Rect(panel_r.x + 1, panel_r.y + 1,
                            panel_r.w - 2, HEADER_H + 8)
        rrect(self.display, PANEL2, hdr_r, r=9)

        # Build + draw pills (category left, sort right)
        self._build_pill_rects()
        self.draw_pills()

        # Separator below header
        sep_y = GRID_CLIP_Y - 4
        pygame.draw.line(self.display, BORDER,
                         (panel_r.x + 4, sep_y), (panel_r.right - 4, sep_y), 1)

        # Scroll hint + nav indicator (top-right of header)
        hint_x = panel_r.right - 80
        hint_y = GRID_Y + (HEADER_H - 14) // 2 + 2
        if self.grid._max_scroll > 0:
            self._txt("scroll ↕", hint_x, hint_y, DIM, "tiny")
        if self._nav_mode == "keys" and self.cursor_idx >= 0:
            row        = self.cursor_idx // COLS + 1
            total_rows = max(1, (count + COLS - 1) // COLS)
            nav_s = self.fonts["tiny"].render(
                f"{self.cursor_idx + 1}/{count}  r{row}/{total_rows}",
                True, BLUE
            )
            self.display.blit(nav_s, (hint_x - nav_s.get_width() - 8, hint_y))

        mx, my = pygame.mouse.get_pos()
        self.grid.draw_clip_start()
        for i, card in enumerate(self.filtered):
            pos = self.grid.card_pos(i)
            cr  = self.grid.clip_rect
            if cr.top - CARD_H <= pos[1] <= cr.bottom:
                hov = (self._nav_mode == "mouse" and
                       pos[0] <= mx <= pos[0] + CARD_W and
                       pos[1] <= my <= pos[1] + CARD_H and
                       cr.collidepoint(mx, my))
                self.draw_card_tile(card, i, pos, hovered=hov)
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
        pw = SIDEBAR_W - 28

        # ── Card preview ──────────────────────────────────────────────
        card = self.selected_card
        if card is not None:
            cat_col_p = CATEGORY_COLORS.get(card["category"], BLUE)

            pygame.draw.rect(self.display, cat_col_p,
                             pygame.Rect(sx + 6, cy, pw, 6),
                             border_top_left_radius=8, border_top_right_radius=8)

            iw = pw - 8
            ih = int(iw * 1.0)
            img = load_image(card["image"], iw, ih)
            self.display.blit(img, (sx + 10, cy + 8))
            cy += ih + 14

            ns = self.fonts["large"].render(card["name"], True, WHITE)
            if ns.get_width() > pw - 8:
                ns = self.fonts["normal"].render(card["name"], True, WHITE)
            self.display.blit(ns, (sx + 6 + pw // 2 - ns.get_width() // 2, cy))
            cy += ns.get_height() + 4

            cat_s = self.fonts["small"].render(card["category"].upper(), True, cat_col_p)
            self.display.blit(cat_s, (sx + 6 + pw // 2 - cat_s.get_width() // 2, cy))
            cy += cat_s.get_height() + 8

            value = card.get("value", None)
            if value is not None:
                orb_r  = 20
                orb_cx = sx + 6 + pw // 2
                orb_cy = cy + orb_r
                draw_value_orb(self.display, value, orb_cx, orb_cy,
                               cat_col_p, self.fonts["normal"], orb_r)
                cy += orb_r * 2 + 10

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

            # Card index / position info when navigating by keys
            if self._nav_mode == "keys" and self.cursor_idx >= 0:
                pygame.draw.line(self.display, BORDER,
                                 (sx + 12, cy), (sx + 6 + pw - 6, cy), 1)
                cy += 6
                pos_s = self.fonts["tiny"].render(
                    f"Card {self.cursor_idx + 1} of {len(self.filtered)}",
                    True, DIM
                )
                self.display.blit(pos_s, (sx + 6 + pw // 2 - pos_s.get_width() // 2, cy))
                cy += pos_s.get_height() + 4

            pygame.draw.line(self.display, BORDER, (sx, cy + 4), (WIDTH - 4, cy + 4), 1)
            cy += 12
        else:
            hint_r = pygame.Rect(sx + 6, cy, pw, 60)
            rrect(self.display, PANEL2, hint_r, r=8)
            t = self.fonts["small"].render("Click a card or use ↑↓←→", True, MUTED)
            self.display.blit(t, (hint_r.centerx - t.get_width() // 2,
                                  hint_r.centery - t.get_height() // 2))
            cy += 72

        # ── Controls ──────────────────────────────────────────────────
        controls = [
            ("↑↓←→",  "Navigate cards"),
            ("Enter",  "Select card"),
            ("PgUp/Dn","Page through"),
            ("Home",   "First card"),
            ("End",    "Last card"),
            ("Tab",    "Next category"),
            ("ESC",    "Main menu"),
            ("D",      "Deck Manager"),
            ("R",      "Reset / All"),
            ("X",      "Random card"),
            ("F",      "Cycle sort"),
            ("1–7",    "Jump category"),
        ]
        for key, desc in controls:
            if cy + 28 > HEIGHT + self.sidebar_scroll_y - 10: break
            kr = pygame.Rect(sx + 6, cy, 42, 20)
            rrect(self.display, (32, 44, 62), kr, r=4)
            ks = self.fonts["tiny"].render(key, True, BLUE)
            self.display.blit(ks, (kr.centerx - ks.get_width() // 2, kr.y + 3))
            self._txt(desc, sx + 54, cy + 2, MUTED, "small")
            cy += 26

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
            self._txt(str(count), sx + 110, cy, DIM, "small")
            cy += 20

        pygame.draw.line(self.display, BORDER, (sx, cy + 4), (WIDTH - 4, cy + 4), 1)
        cy += 12

        # ── Sort indicator ────────────────────────────────────────────
        self._txt("Sort", sx + 6, cy, WHITE, "small"); cy += 20
        for mode in SORT_MODES:
            active = (mode == self.sort_mode)
            col    = AMBER if active else MUTED
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
        if self._nav_mode == "keys" and self.cursor_idx >= 0:
            self._txt(f"Cursor   {self.cursor_idx + 1}", sx + 6, cy, BLUE, "small"); cy += 20

        pygame.draw.line(self.display, BORDER, (sx, cy + 4), (WIDTH - 4, cy + 4), 1)
        cy += 12

        # ── Status ───────────────────────────────────────────────────
        if self.status:
            col = (GREEN if any(w in self.status for w in ("Viewing","Reset","Loaded","Random","Sorted"))
                   else RED if any(w in self.status for w in ("error","No"))
                   else TEAL)
            self._txt(self.status, sx + 6, cy, col, "normal")
            cy += 28

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

        if self._nav_mode == "keys":
            hint_text = "↑↓←→ navigate  ·  Enter select  ·  Tab/click category pills  ·  F sort  ·  X random"
            hint_col  = BLUE
        else:
            hint_text = "click category pills to filter  ·  F sort  ·  X random  ·  ↑↓←→ key-nav"
            hint_col  = DIM

        hint = self.fonts["small"].render(hint_text, True, hint_col)
        self.display.blit(hint, (WIDTH // 2 - hint.get_width() // 2, 18))

        # Nav mode badge
        mode_s = self.fonts["tiny"].render(
            "⌨ KEYS" if self._nav_mode == "keys" else "🖱 MOUSE",
            True, BLUE if self._nav_mode == "keys" else MUTED
        )
        self.display.blit(mode_s, (WIDTH - SIDEBAR_W - mode_s.get_width() - 20, 18))

    def draw(self):
        self.tick_status()
        self.display.fill(BG)
        self.draw_header()
        self.draw_grid()      # pills are drawn inside draw_grid
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