import os
import re
import datetime
import pygame

# =====================
# Files
# =====================
SAVE_FILE    = "deck_manager.txt"
HISTORY_FILE = "history_deck_manager.txt"

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
CARD_GREY     = (18,  20,  26)
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
OVERLAY       = (8,   10,  16, 225)

# Category accent colours — matches card_viewer.py
CATEGORY_COLORS = {
    "Core":    TEAL,
    "Toon":    PURPLE,
    "Special": AMBER,
    "Exodia":  RED,
    "Units":   (75,  175, 120),
    "Spells":  (180, 100, 220),
    "AA":      (220, 140,  60),
}

CARD_W, CARD_H = 108, 148
MAX_DECK       = 30
STATUS_DUR     = 150

# Deck selector overlay
DS_W, DS_H = 260, 360
DS_GAP     = 44

# =====================
# Layout
# =====================
PAD          = 14
SIDEBAR_X    = 1490
TABS_Y       = 8
TABS_H       = 44

DECK_LABEL_Y = TABS_Y + TABS_H + 10
DECK_Y       = DECK_LABEL_Y + 22

COLL_LABEL_Y = 590
COLL_Y       = COLL_LABEL_Y + 22

DECK_PANEL_W = SIDEBAR_X - PAD * 2
COLL_PANEL_W = DECK_PANEL_W
DECK_PANEL_X = PAD
COLL_PANEL_X = PAD

CARD_COLS    = 11
CARD_CW      = CARD_W + 10
CARD_CH      = CARD_H + 10

DECK_VIS_ROWS = 3
COLL_VIS_ROWS = 3
DECK_VIS_H    = DECK_VIS_ROWS * CARD_CH
COLL_VIS_H    = COLL_VIS_ROWS * CARD_CH

DECK_DEFS = [
    {"key": "a", "label": "Deck A", "image": "assets/deck_a_image.png"},
    {"key": "b", "label": "Deck B", "image": "assets/deck_b_image.png"},
    {"key": "c", "label": "Deck C", "image": "assets/deck_c_image.png"},
]

# =====================
# Card data — from cards.py
# =====================
import cards as _cards_module
ALL_CARDS = _cards_module.ALL_CARDS   # list of dicts: {name, image, category, desc}


# =====================
# Image cache
# =====================
_img_cache = {}

def load_card_image(path, w, h):
    key = (path, w, h)
    if key in _img_cache:
        return _img_cache[key]
    try:
        img = pygame.image.load(path).convert_alpha()
        img = pygame.transform.smoothscale(img, (w, h))
    except Exception:
        img = pygame.Surface((w, h), pygame.SRCALPHA)
        img.fill((38, 44, 60, 220))
    _img_cache[key] = img
    return img


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
    words = text.split()
    lines, line = [], ""
    for w in words:
        test = (line + " " + w).strip()
        if font.size(test)[0] <= max_w:
            line = test
        else:
            if line:
                lines.append(line)
            line = w
    if line:
        lines.append(line)
    return lines


def draw_value_orb(surf, value, cx, cy, accent, font, orb_r=11):
    """Concentric-ring orb with a numeric value centred inside."""
    pygame.draw.circle(surf, accent, (cx, cy), orb_r)
    pygame.draw.circle(surf, PANEL2,  (cx, cy), orb_r - 3)
    pygame.draw.circle(surf, accent, (cx, cy), orb_r - 6)
    vs = font.render(str(value), True, WHITE)
    surf.blit(vs, (cx - vs.get_width() // 2, cy - vs.get_height() // 2))


def card_accent(card_dict):
    """Return accent colour for a card dict based on its category."""
    return CATEGORY_COLORS.get(card_dict.get("category", ""), BLUE)


# =====================
# Scrollable card grid
# =====================
class CardGrid:
    def __init__(self, display, clip_rect, cols=CARD_COLS):
        self.display     = display
        self.clip_rect   = clip_rect
        self.cols        = cols
        self.scroll_y    = 0
        self._max_scroll = 0

    def scroll(self, dy):
        self.scroll_y = clamp(self.scroll_y + dy, 0, max(0, self._max_scroll))

    def reset_scroll(self):
        self.scroll_y = 0

    def card_pos(self, idx):
        col = idx % self.cols
        row = idx // self.cols
        return (self.clip_rect.x + col * CARD_CW,
                self.clip_rect.y + row * CARD_CH - self.scroll_y)

    def update_max_scroll(self, count):
        rows = max(1, (count + self.cols - 1) // self.cols)
        self._max_scroll = max(0, rows * CARD_CH - self.clip_rect.height)

    def card_at(self, pos, count):
        if not self.clip_rect.collidepoint(pos):
            return None
        for i in range(count):
            x, y = self.card_pos(i)
            if x <= pos[0] <= x + CARD_W and y <= pos[1] <= y + CARD_H:
                return i
        return None

    def draw_clip_start(self):
        self.display.set_clip(self.clip_rect)

    def draw_clip_end(self):
        self.display.set_clip(None)


# =====================
# Deck Selector Overlay
# =====================
class DeckSelector:
    SELECT_KEYS = {
        pygame.K_1: 0, pygame.K_a: 0,
        pygame.K_2: 1, pygame.K_b: 1,
        pygame.K_3: 2, pygame.K_c: 2,
    }

    def __init__(self, display, fonts):
        self.display = display
        self.fonts   = fonts
        self.active  = False
        self.hovered = None
        DS_Y         = (HEIGHT - DS_H) // 2
        self.DS_Y    = DS_Y

        self.images = [self._load(d["image"], DS_W - 30, DS_H - 80) for d in DECK_DEFS]
        total_w     = len(DECK_DEFS) * DS_W + (len(DECK_DEFS) - 1) * DS_GAP
        sx          = (WIDTH - total_w) // 2
        self.rects  = [pygame.Rect(sx + i * (DS_W + DS_GAP), DS_Y, DS_W, DS_H)
                       for i in range(len(DECK_DEFS))]
        self.dim = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.dim.fill(OVERLAY)

    def _load(self, path, mw, mh):
        if not os.path.exists(path):
            return None
        try:
            img    = pygame.image.load(path).convert_alpha()
            iw, ih = img.get_size()
            s      = min(mw / iw, mh / ih)
            return pygame.transform.smoothscale(img, (int(iw * s), int(ih * s)))
        except Exception:
            return None

    def open(self):
        self.active = True;  self.hovered = None

    def close(self):
        self.active = False

    def handle_event(self, e):
        if not self.active:
            return None
        if e.type == pygame.MOUSEMOTION:
            self.hovered = next((i for i, r in enumerate(self.rects)
                                 if r.collidepoint(e.pos)), None)
        elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            for i, r in enumerate(self.rects):
                if r.collidepoint(e.pos):
                    self.close(); return i
        elif e.type == pygame.KEYDOWN:
            if e.key in (pygame.K_ESCAPE, pygame.K_d):
                self.close(); return -1
            idx = self.SELECT_KEYS.get(e.key)
            if idx is not None:
                self.close(); return idx
        return None

    def draw(self):
        if not self.active:
            return
        self.display.blit(self.dim, (0, 0))
        f, fs, fl = self.fonts["normal"], self.fonts["small"], self.fonts["large"]

        t = fl.render("Choose a Deck", True, WHITE)
        self.display.blit(t, (WIDTH // 2 - t.get_width() // 2, self.DS_Y - 72))
        h = fs.render("1/A  2/B  3/C  or click  ·  ESC cancel", True, MUTED)
        self.display.blit(h, (WIDTH // 2 - h.get_width() // 2, self.DS_Y - 36))

        for i, (d, r) in enumerate(zip(DECK_DEFS, self.rects)):
            hov    = (self.hovered == i)
            bg     = (40, 52, 74) if hov else (24, 28, 40)
            border = BLUE if hov else BORDER
            rrect(self.display, bg, r, r=10)
            rrect(self.display, border, r, r=10, bw=2)

            br = pygame.Rect(r.x + 8, r.y + 8, 54, 20)
            rrect(self.display, (28, 56, 96), br, r=4)
            bs = fs.render(f"{i+1}/{d['key'].upper()}", True, BLUE)
            self.display.blit(bs, (br.x + 4, br.y + 2))

            img = self.images[i]
            if img:
                iw, ih = img.get_size()
                self.display.blit(img, (r.x + (DS_W - iw) // 2, r.y + 36))
            else:
                ph = pygame.Rect(r.x + 12, r.y + 36, DS_W - 24, DS_H - 76)
                rrect(self.display, CARD_BG, ph, r=6)
                ni = fs.render("No image", True, MUTED)
                self.display.blit(ni, (ph.centerx - ni.get_width() // 2,
                                       ph.centery - ni.get_height() // 2))

            lb = f.render(d["label"], True, WHITE if hov else MUTED)
            self.display.blit(lb, (r.x + DS_W // 2 - lb.get_width() // 2,
                                   r.y + DS_H - 30))


# =====================
# Card Preview (rendered inside sidebar)
# =====================
class CardPreview:
    def __init__(self, display, fonts):
        self.display = display
        self.fonts   = fonts
        self.card    = None   # full card dict  {name, image, category, desc}
        self.count   = 0

    def set_card(self, card_dict, count=0):
        self.card  = card_dict
        self.count = count

    def draw_in_sidebar(self, sx, cy, preview_w):
        """Draw preview at (sx, cy). Returns updated cy."""
        fs = self.fonts["small"]
        fn = self.fonts["normal"]
        fl = self.fonts["large"]
        fd = self.fonts.get("desc", fs)

        if self.card is None:
            t  = fs.render("Hover a card to preview", True, MUTED)
            t2 = fs.render("it here", True, DIM)
            self.display.blit(t,  (sx + preview_w // 2 - t.get_width()  // 2, cy + 8))
            self.display.blit(t2, (sx + preview_w // 2 - t2.get_width() // 2, cy + 26))
            return cy + 50

        accent = card_accent(self.card)

        # Accent bar
        pygame.draw.rect(self.display, accent,
                         pygame.Rect(sx, cy, preview_w, 5),
                         border_top_left_radius=6, border_top_right_radius=6)
        cy += 7

        # Card image
        iw = preview_w - 4
        ih = int(iw * 0.9)
        img = load_card_image(self.card["image"], iw, ih)
        self.display.blit(img, (sx + 2, cy))
        cy += ih + 6

        # Name
        ns = fl.render(self.card["name"], True, WHITE)
        if ns.get_width() > preview_w:
            ns = fn.render(self.card["name"], True, WHITE)
        self.display.blit(ns, (sx + preview_w // 2 - ns.get_width() // 2, cy))
        cy += ns.get_height() + 4

        # Category badge
        cat_s = fs.render(self.card.get("category", "").upper(), True, accent)
        self.display.blit(cat_s, (sx + preview_w // 2 - cat_s.get_width() // 2, cy))
        cy += cat_s.get_height() + 6

        # Value orb
        value = self.card.get("value", None)
        if value is not None:
            orb_r   = 18
            orb_cx  = sx + preview_w // 2
            orb_cy  = cy + orb_r
            # Outer ring using accent colour
            pygame.draw.circle(self.display, accent,     (orb_cx, orb_cy), orb_r)
            pygame.draw.circle(self.display, PANEL2,     (orb_cx, orb_cy), orb_r - 3)
            pygame.draw.circle(self.display, accent,     (orb_cx, orb_cy), orb_r - 7)
            vs = fn.render(str(value), True, WHITE)
            self.display.blit(vs, (orb_cx - vs.get_width() // 2,
                                   orb_cy - vs.get_height() // 2))
            cy += orb_r * 2 + 8

        # In-deck count
        if self.count > 0:
            ct = fn.render(f"×{self.count} in deck", True, TEAL)
        else:
            ct = fs.render("not in deck", True, MUTED)
        self.display.blit(ct, (sx + preview_w // 2 - ct.get_width() // 2, cy))
        cy += ct.get_height() + 6

        # Divider
        pygame.draw.line(self.display, BORDER, (sx + 4, cy), (sx + preview_w - 4, cy), 1)
        cy += 6

        # Description
        desc = self.card.get("desc", "")
        if desc:
            for line in wrap_text(fd, desc, preview_w - 8):
                ds = fd.render(line, True, MUTED)
                self.display.blit(ds, (sx + 4, cy))
                cy += ds.get_height() + 2
            cy += 4

        # Divider after
        pygame.draw.line(self.display, BORDER, (sx + 4, cy), (sx + preview_w - 4, cy), 1)
        cy += 8
        return cy



# =====================
# Hand Simulator
# =====================
class HandSimulator:
    """
    Replaces the collection area when active.
    H   – open / close
    D   – draw one more card  (also +1 Draw button)
    R   – redraw full opening hand
    B   – return to collection
    """
    HAND_SIZE = 7

    def __init__(self, display, fonts, card_dict_fn):
        self.display   = display
        self.fonts     = fonts
        self.card_dict = card_dict_fn
        self.active    = False
        self.hand      = []        # list of card name strings
        self.draw_pile = []
        self.last_drawn_idx = -1   # index of most-recently drawn card (-1 = none)
        self._btn_rects = {}
        self._card_positions = []

    # ------------------------------------------------------------------
    def open(self, deck):
        self.active = True
        self._shuffle_deck(deck)
        self._draw_opening_hand()

    def close(self):
        self.active         = False
        self.hand           = []
        self.draw_pile      = []
        self.last_drawn_idx = -1

    def _shuffle_deck(self, deck):
        import random
        pile = []
        for name, count in deck.items():
            pile.extend([name] * count)
        random.shuffle(pile)
        self.draw_pile = pile

    def _draw_opening_hand(self):
        self.hand = []
        for _ in range(self.HAND_SIZE):
            if self.draw_pile:
                self.hand.append(self.draw_pile.pop())
        self.last_drawn_idx = len(self.hand) - 1 if self.hand else -1

    def draw_one(self):
        """Draw one card from the pile into the hand. Returns True if successful."""
        if self.draw_pile:
            self.hand.append(self.draw_pile.pop())
            self.last_drawn_idx = len(self.hand) - 1
            return True
        self.last_drawn_idx = -1
        return False

    def redraw(self, deck):
        self._shuffle_deck(deck)
        self._draw_opening_hand()

    # ------------------------------------------------------------------
    def _layout(self, panel_r):
        """
        Calculate (col, row) grid positions for each card in the hand.
        Cards wrap into rows to fill the panel width, with a max card
        size chosen so they always fit without overflow.
        """
        if not self.hand:
            self._card_positions = []
            return

        count    = len(self.hand)
        # Available width inside the panel (leave room for scrollbar gutter)
        avail_w  = panel_r.width - 24
        avail_h  = COLL_VIS_H - 4

        # Try to fit in 1 row first, then 2, then 3
        for rows in (1, 2, 3):
            cols      = -(-count // rows)   # ceil div
            cw        = min(CARD_W, (avail_w - (cols - 1) * 8) // cols)
            ch        = int(cw * (CARD_H / CARD_W))
            row_h     = ch + 8
            if row_h * rows <= avail_h:
                break

        # Centre the grid inside the panel
        total_card_w = cols * cw + (cols - 1) * 8
        total_card_h = rows * row_h
        ox = panel_r.x + (panel_r.width - total_card_w) // 2
        oy = COLL_Y + (avail_h - total_card_h) // 2

        self._card_positions = []
        self._card_size      = (cw, ch)
        for i in range(count):
            c = i % cols
            r = i // cols
            self._card_positions.append((ox + c * (cw + 8), oy + r * row_h))

    # ------------------------------------------------------------------
    def draw_area(self, draw_card_widget_fn):
        d  = self.display
        fs = self.fonts["small"]
        fn = self.fonts["normal"]
        ft = self.fonts.get("tiny", fs)

        panel_r = pygame.Rect(COLL_PANEL_X - PAD, COLL_LABEL_Y - 4,
                              COLL_PANEL_W + PAD + 12, COLL_VIS_H + 34)
        rrect(d, PANEL, panel_r, r=10)
        rrect(d, BORDER, panel_r, r=10, bw=1)

        # ── Header row ────────────────────────────────────────────────
        lx, ly = COLL_PANEL_X, COLL_LABEL_Y
        hs = fn.render("HAND SIMULATOR", True, TEAL)
        d.blit(hs, (lx, ly))

        pile_col = MUTED if self.draw_pile else RED
        pile_lbl = f"{len(self.draw_pile)} in pile" if self.draw_pile else "pile empty"
        pt = fs.render(pile_lbl, True, pile_col)
        d.blit(pt, (lx + hs.get_width() + 12, ly + 2))

        hand_t = fs.render(f"{len(self.hand)} cards in hand", True, MUTED)
        d.blit(hand_t, (lx + hs.get_width() + 12 + pt.get_width() + 16, ly + 2))

        # ── Buttons ───────────────────────────────────────────────────
        mx, my  = pygame.mouse.get_pos()
        buttons = [
            ("B  Back",       MUTED,  80),
            ("+1  Draw  [D]", TEAL,  110),
            ("R  Redraw",     AMBER, 110),
        ]
        self._btn_rects = {}
        bx = panel_r.right - 6
        for label, col, w in buttons:
            bx -= w + 6
            br  = pygame.Rect(bx, ly - 2, w, 22)
            hov = br.collidepoint(mx, my)
            disabled = ("Draw" in label and not self.draw_pile)
            bg  = (35, 48, 68) if (hov and not disabled) else (22, 26, 36)
            bc  = col if not disabled else DIM
            rrect(d, bg, br, r=5)
            rrect(d, bc, br, r=5, bw=1, bc=bc)
            ts = fs.render(label, True, (WHITE if hov and not disabled else (bc)))
            d.blit(ts, (br.x + br.w // 2 - ts.get_width() // 2,
                        br.y + br.h // 2 - ts.get_height() // 2))
            self._btn_rects[label] = br

        # ── Empty hand ────────────────────────────────────────────────
        if not self.hand:
            msg = fn.render("Deck is empty — nothing to draw", True, MUTED)
            d.blit(msg, (panel_r.centerx - msg.get_width() // 2,
                         COLL_Y + COLL_VIS_H // 2 - msg.get_height() // 2))
            return

        # ── Card grid ─────────────────────────────────────────────────
        self._layout(panel_r)
        cw, ch = getattr(self, "_card_size", (CARD_W, CARD_H))

        for i, (name, pos) in enumerate(zip(self.hand, self._card_positions)):
            cd = self.card_dict(name)
            if cd:
                # Temporarily override global CARD_W/CARD_H for widget sizing
                # We draw manually here to support variable card size
                rx, ry  = pos
                hov     = rx <= mx <= rx + cw and ry <= my <= ry + ch
                is_new  = (i == self.last_drawn_idx)
                accent  = card_accent(cd) if cd else BLUE

                if is_new:
                    bg, bord = CARD_HOV, accent
                elif hov:
                    bg, bord = CARD_HOV, CARD_BORD_ACT
                else:
                    bg, bord = CARD_BG, CARD_BORD

                r = pygame.Rect(rx, ry, cw, ch)
                rrect(d, bg, r, r=6)
                rrect(d, bord, r, r=6, bw=2 if is_new else 1)

                # Glow ring for newest drawn card
                if is_new:
                    rrect(d, (*accent, 0), r, r=6, bw=3, bc=accent)

                # Image
                img_h = ch - 24
                img   = load_card_image(cd["image"], cw - 4, img_h)
                d.blit(img, (rx + 2, ry + 5))

                # Accent stripe
                stripe = pygame.Rect(rx + 1, ry + 1, cw - 2, 4)
                pygame.draw.rect(d, accent, stripe,
                                 border_top_left_radius=5, border_top_right_radius=5)

                # Name
                ns = ft.render(cd["name"], True, WHITE)
                if ns.get_width() > cw - 4:
                    ns = pygame.font.Font(None, 14).render(cd["name"], True, WHITE)
                d.blit(ns, (rx + cw // 2 - ns.get_width() // 2, ry + ch - 16))

                # Value orb
                val = cd.get("value", None)
                if val is not None:
                    draw_value_orb(d, val, rx + 10, ry + ch - 12, accent,
                                   self.fonts.get("tiny", ft), orb_r=9)

                # "NEW" badge on last drawn card
                if is_new:
                    nb = pygame.Rect(rx + cw - 32, ry + ch - 20, 30, 16)
                    rrect(d, accent, nb, r=3)
                    nt = ft.render("NEW", True, BG)
                    d.blit(nt, (nb.x + nb.w // 2 - nt.get_width() // 2,
                                nb.y + nb.h // 2 - nt.get_height() // 2))

            # Index badge below card
            idx_s = ft.render(str(i + 1), True, MUTED)
            d.blit(idx_s, (pos[0] + cw // 2 - idx_s.get_width() // 2,
                           pos[1] + ch + 2))

        # ── Empty-pile notice at bottom of panel ──────────────────────
        if not self.draw_pile:
            ep = fs.render("— draw pile exhausted —", True, RED)
            d.blit(ep, (panel_r.centerx - ep.get_width() // 2,
                        panel_r.bottom - 18))

    def handle_click(self, pos, deck):
        for label, br in self._btn_rects.items():
            if br.collidepoint(pos):
                if "Redraw" in label:
                    self.redraw(deck); return "redraw"
                elif "Draw" in label:
                    return "drew" if self.draw_one() else "empty"
                elif "Back" in label:
                    self.close(); return "back"
        return None


# =====================
# Deck Manager
# =====================
class DeckManager:
    def __init__(self, display):
        self.display = display

        self.fonts = {
            "normal": pygame.font.Font(None, 24),
            "small":  pygame.font.Font(None, 20),
            "large":  pygame.font.Font(None, 40),
            "title":  pygame.font.Font(None, 32),
            "desc":   pygame.font.Font(None, 19),
            "tiny":   pygame.font.Font(None, 16),
        }

        # collection is list of card dicts; lookup by name for deck storage
        self.collection   = list(ALL_CARDS)
        self.card_by_name = {c["name"]: c for c in self.collection}
        self.owned_cards  = {c["name"]: 2 for c in self.collection}

        self.decks       = [{}, {}, {}]   # {card_name: count}
        self.active_deck = 0
        self.undo_stacks = [[], [], []]
        self.unsaved     = [False, False, False]

        self.dragging_card = None   # card name string
        self.drag_from     = None
        self.drag_pos      = (0, 0)

        self.status       = ""
        self.status_timer = 0

        self.preview = CardPreview(display, self.fonts)

        deck_clip = pygame.Rect(DECK_PANEL_X, DECK_Y, DECK_PANEL_W, DECK_VIS_H)
        self.deck_grid = CardGrid(display, deck_clip, cols=CARD_COLS)

        coll_clip = pygame.Rect(COLL_PANEL_X, COLL_Y, COLL_PANEL_W, COLL_VIS_H)
        self.coll_grid = CardGrid(display, coll_clip, cols=CARD_COLS)

        self.selector = DeckSelector(display, self.fonts)
        self.hand_sim = HandSimulator(display, self.fonts, self.card_dict)
        self.active_coll_cat = "All"   # collection category filter
        self._preview_idx = -1              # -1 = no selection; used by arrow keys

        self.load_decks()

    # ------------------------------------------------------------------
    @property
    def deck(self):
        return self.decks[self.active_deck]

    @deck.setter
    def deck(self, v):
        self.decks[self.active_deck] = v

    @property
    def undo_stack(self):
        return self.undo_stacks[self.active_deck]

    def deck_name(self):
        return DECK_DEFS[self.active_deck]["label"]

    def card_dict(self, name):
        return self.card_by_name.get(name)

    def filtered_collection(self):
        if self.active_coll_cat == "All":
            return self.collection
        return [c for c in self.collection if c.get("category") == self.active_coll_cat]

    # =====================
    # File I/O
    # =====================
    def load_decks(self):
        if not os.path.exists(SAVE_FILE):
            return
        try:
            current_idx = None
            with open(SAVE_FILE) as f:
                for raw in f:
                    line = raw.strip()
                    if not line or line.startswith("#"):
                        continue
                    hdr = re.match(r"^\[(.+)\]$", line)
                    if hdr:
                        label = hdr.group(1)
                        current_idx = next(
                            (i for i, d in enumerate(DECK_DEFS) if d["label"] == label), None
                        )
                        continue
                    if current_idx is not None and line != "(empty)":
                        m = re.match(r"^(.+?)\s+x(\d+)$", line)
                        if m:
                            name, count = m.group(1).strip(), int(m.group(2))
                            if name in self.card_by_name:
                                self.decks[current_idx][name] = count
            self.unsaved = [False, False, False]
            self.set_status("Loaded from file")
        except Exception as e:
            self.set_status(f"Load error: {e}")

    def save_deck(self):
        lines = []
        for i, d in enumerate(DECK_DEFS):
            lines.append(f"[{d['label']}]")
            dk = self.decks[i]
            for name, count in sorted(dk.items()):
                lines.append(f"  {name} x{count}")
            if not dk:
                lines.append("  (empty)")
            lines.append("")
        text = "\n".join(lines).rstrip() + "\n"
        with open(SAVE_FILE, "w") as f:
            f.write(text)
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(HISTORY_FILE, "a") as f:
            f.write(f"=== Saved {ts} ===\n{text}\n")
        self.unsaved = [False, False, False]
        self.set_status("Saved!")

    # =====================
    # Events
    # =====================
    def handle_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return False

            if self.selector.active:
                r = self.selector.handle_event(e)
                if r is not None and r >= 0:
                    self._switch_deck(r)
                continue

            if e.type == pygame.MOUSEWHEEL:
                mx, my = pygame.mouse.get_pos()
                dy = -e.y * 30
                if self.deck_grid.clip_rect.collidepoint(mx, my):
                    self.deck_grid.scroll(dy)
                elif self.coll_grid.clip_rect.collidepoint(mx, my):
                    self.coll_grid.scroll(dy)

            elif e.type == pygame.MOUSEBUTTONDOWN:
                if not self.hand_sim.active and e.button == 1:
                    for cat, pr in getattr(self, "_coll_cat_pills", []):
                        if pr.collidepoint(e.pos):
                            self.active_coll_cat = cat
                            self._preview_idx    = -1
                            self.coll_grid.reset_scroll()
                            break
                if self.hand_sim.active and e.button == 1:
                    result = self.hand_sim.handle_click(e.pos, self.deck)
                    if result == "back":
                        self.set_status("Back to collection")
                    elif result == "redraw":
                        self.set_status("Hand redrawn!")
                    elif result == "drew":
                        self.set_status(f"Drew — {len(self.hand_sim.hand)} cards in hand")
                    elif result == "empty":
                        self.set_status("Draw pile empty!")
                elif e.button == 3 and not self.hand_sim.active:
                    self._right_click(e.pos)
                elif e.button == 1 and not self.hand_sim.active:
                    self.start_drag(e.pos)

            elif e.type == pygame.MOUSEBUTTONUP:
                if e.button == 1 and not self.hand_sim.active:
                    self.end_drag(e.pos)

            elif e.type == pygame.MOUSEMOTION:
                self.drag_pos = e.pos
                self._update_preview_hover(e.pos)

            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    try:
                        import cardgame; cardgame.main()
                    except Exception:
                        return False
                elif e.key == pygame.K_v:
                    try:
                        import card_viewer; card_viewer.main()
                    except Exception:
                        pass
                elif e.key == pygame.K_d:
                    self.selector.open()
                elif e.key == pygame.K_z:
                    self.undo()
                elif e.key == pygame.K_c:
                    self.clear_deck()
                elif e.key == pygame.K_s:
                    self.save_deck()
                elif e.key == pygame.K_h:
                    if self.hand_sim.active:
                        self.hand_sim.close()
                    else:
                        if self.total_cards() == 0:
                            self.set_status("Deck is empty!")
                        else:
                            self.hand_sim.open(self.deck)
                            self.set_status("Hand drawn!")
                elif e.key == pygame.K_r:
                    if self.hand_sim.active:
                        self.hand_sim.redraw(self.deck)
                        self.set_status("Hand redrawn!")
                elif e.key == pygame.K_t:
                    if self.hand_sim.active:
                        drew = self.hand_sim.draw_one()
                        if drew:
                            self.set_status(f"Drew — {len(self.hand_sim.hand)} cards in hand")
                        else:
                            self.set_status("Draw pile empty!")
                elif e.key == pygame.K_b:
                    if self.hand_sim.active:
                        self.hand_sim.close()
                        self.set_status("Back to collection")
                elif e.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN):
                    self._arrow_navigate(e.key)
                elif e.key == pygame.K_SPACE:
                    if self.hand_sim.active:
                        drew = self.hand_sim.draw_one()
                        if drew:
                            self.set_status(f"Drew {self.hand_sim.hand[-1]}  —  {len(self.hand_sim.hand)} in hand")
                        else:
                            self.set_status("Draw pile empty!")

        return True

    def _update_preview_hover(self, pos):
        for i, cd in enumerate(self.collection):
            cx, cy = self.coll_grid.card_pos(i)
            if (cx <= pos[0] <= cx + CARD_W and cy <= pos[1] <= cy + CARD_H
                    and self.coll_grid.clip_rect.collidepoint(pos)):
                self.preview.set_card(cd, self.deck.get(cd["name"], 0))
                return
        deck_list = self.expand_deck()
        for i, name in enumerate(deck_list):
            cx, cy = self.deck_grid.card_pos(i)
            if (cx <= pos[0] <= cx + CARD_W and cy <= pos[1] <= cy + CARD_H
                    and self.deck_grid.clip_rect.collidepoint(pos)):
                self.preview.set_card(self.card_dict(name), self.deck.get(name, 0))
                return

    def _switch_deck(self, idx):
        self.active_deck  = idx
        self._preview_idx = -1
        self.deck_grid.reset_scroll()
        self.set_status(f"Switched to {self.deck_name()}")

    def _arrow_navigate(self, key):
        """Move the preview selection through the collection or hand using arrow keys,
        and auto-scroll the relevant grid so the selected card stays visible."""
        if self.hand_sim.active:
            cards = self.hand_sim.hand
            # Navigate hand
            if not cards:
                return
            if self._preview_idx < 0:
                self._preview_idx = 0
            else:
                if key == pygame.K_RIGHT:
                    self._preview_idx = (self._preview_idx + 1) % len(cards)
                elif key == pygame.K_LEFT:
                    self._preview_idx = (self._preview_idx - 1) % len(cards)
            name = cards[self._preview_idx]
            cd   = self.card_dict(name)
            if cd:
                self.preview.set_card(cd, self.deck.get(name, 0))
        else:
            filt = self.filtered_collection()
            if not filt:
                return
            cols = CARD_COLS
            if self._preview_idx < 0:
                self._preview_idx = 0
            else:
                if key == pygame.K_RIGHT:
                    self._preview_idx = min(self._preview_idx + 1, len(filt) - 1)
                elif key == pygame.K_LEFT:
                    self._preview_idx = max(self._preview_idx - 1, 0)
                elif key == pygame.K_DOWN:
                    self._preview_idx = min(self._preview_idx + cols, len(filt) - 1)
                elif key == pygame.K_UP:
                    self._preview_idx = max(self._preview_idx - cols, 0)

            cd = filt[self._preview_idx]
            self.preview.set_card(cd, self.deck.get(cd["name"], 0))

            # Auto-scroll collection grid so card is visible
            row        = self._preview_idx // cols
            card_top   = row * CARD_CH
            card_bot   = card_top + CARD_H
            vis_top    = self.coll_grid.scroll_y
            vis_bot    = vis_top + self.coll_grid.clip_rect.height
            if card_top < vis_top:
                self.coll_grid.scroll_y = clamp(card_top, 0, self.coll_grid._max_scroll)
            elif card_bot > vis_bot:
                self.coll_grid.scroll_y = clamp(
                    card_bot - self.coll_grid.clip_rect.height,
                    0, self.coll_grid._max_scroll
                )

    # =====================
    # Interactions
    # =====================
    def _right_click(self, pos):
        idx = self.coll_grid.card_at(pos, len(self.collection))
        if idx is not None:
            cd = self.collection[idx]
            name = cd["name"]
            if self.total_cards() >= MAX_DECK:
                self.set_status("Deck Full!")
            elif self.copies_avail(name) <= 0:
                self.set_status("No copies left!")
            else:
                self.push_undo()
                self.add_card(name)
                self.preview.set_card(cd, self.deck.get(name, 0))
                self.set_status(f"Added {name}")
            return
        deck_list = self.expand_deck()
        idx = self.deck_grid.card_at(pos, len(deck_list))
        if idx is not None:
            self.remove_card(deck_list[idx])

    def start_drag(self, pos):
        idx = self.coll_grid.card_at(pos, len(self.collection))
        if idx is not None:
            cd   = self.collection[idx]
            name = cd["name"]
            if self.copies_avail(name) > 0:
                self.dragging_card = name
                self.drag_from     = "collection"
                self.preview.set_card(cd, self.deck.get(name, 0))
            else:
                self.set_status("No copies left!")
            return
        deck_list = self.expand_deck()
        idx = self.deck_grid.card_at(pos, len(deck_list))
        if idx is not None:
            name = deck_list[idx]
            self.dragging_card = name
            self.drag_from     = "deck"
            self.push_undo()
            self.deck[name] -= 1
            if self.deck[name] <= 0:
                del self.deck[name]
            self.preview.set_card(self.card_dict(name), self.deck.get(name, 0))

    def end_drag(self, pos):
        if not self.dragging_card:
            return
        if self.deck_grid.clip_rect.collidepoint(pos):
            if self.total_cards() >= MAX_DECK:
                self.set_status("Deck Full!")
                if self.drag_from == "deck":
                    self.deck[self.dragging_card] = self.deck.get(self.dragging_card, 0) + 1
            else:
                if self.drag_from == "collection":
                    self.push_undo()
                self.add_card(self.dragging_card)
                cd = self.card_dict(self.dragging_card)
                if cd:
                    self.preview.set_card(cd, self.deck.get(self.dragging_card, 0))
                self.set_status(f"Added {self.dragging_card}")
        else:
            if self.drag_from == "deck":
                self.deck[self.dragging_card] = self.deck.get(self.dragging_card, 0) + 1
                self.set_status("Cancelled")
        self.dragging_card = None
        self.drag_from     = None

    # =====================
    # Deck Logic
    # =====================
    def add_card(self, name):
        self.deck[name] = self.deck.get(name, 0) + 1
        self.unsaved[self.active_deck] = True

    def remove_card(self, name):
        if name and name in self.deck:
            self.push_undo()
            self.deck[name] -= 1
            if self.deck[name] <= 0:
                del self.deck[name]
            self.unsaved[self.active_deck] = True
            self.set_status(f"Removed {name}")

    def clear_deck(self):
        if self.deck:
            self.push_undo()
            self.deck = {}
            self.unsaved[self.active_deck] = True
            self.set_status("Deck Cleared!")

    def expand_deck(self):
        r = []
        for name, count in self.deck.items():
            r.extend([name] * count)
        return r

    def total_cards(self):
        return sum(self.deck.values())

    def copies_avail(self, name):
        return self.owned_cards.get(name, 0) - self.deck.get(name, 0)

    def push_undo(self):
        self.undo_stack.append(self.deck.copy())
        if len(self.undo_stack) > 50:
            self.undo_stack.pop(0)

    def undo(self):
        if self.undo_stack:
            self.deck = self.undo_stack.pop()
            self.set_status("Undo!")

    def set_status(self, msg):
        self.status       = msg
        self.status_timer = STATUS_DUR

    def tick_status(self):
        if self.status_timer > 0:
            self.status_timer -= 1
            if self.status_timer == 0:
                self.status = ""

    # =====================
    # Drawing
    # =====================
    def _txt(self, text, x, y, color=WHITE, fk="normal"):
        s = self.fonts[fk].render(text, True, color)
        self.display.blit(s, (x, y))

    def draw_card_widget(self, card_dict, pos, in_deck=False, greyed=False):
        """Draw a single card tile. card_dict is the full card dict."""
        rx, ry = pos
        mx, my = pygame.mouse.get_pos()
        hov    = rx <= mx <= rx + CARD_W and ry <= my <= ry + CARD_H and not greyed

        if greyed:
            bg, bord = CARD_GREY, (32, 36, 46)
        elif hov:
            bg, bord = CARD_HOV, CARD_BORD_ACT
        else:
            bg, bord = CARD_BG, CARD_BORD

        r = pygame.Rect(rx, ry, CARD_W, CARD_H)
        rrect(self.display, bg, r, r=7)
        rrect(self.display, bord, r, r=7, bw=1)

        # Card image (most of the card face)
        img_h = CARD_H - 28
        img   = load_card_image(card_dict["image"], CARD_W - 4, img_h)
        if greyed:
            grey_surf = img.copy()
            grey_surf.fill((0, 0, 0, 140), special_flags=pygame.BLEND_RGBA_MULT)
            self.display.blit(grey_surf, (rx + 2, ry + 6))
        else:
            self.display.blit(img, (rx + 2, ry + 6))

        # Accent stripe at top (category colour)
        accent = card_accent(card_dict)
        stripe = pygame.Rect(rx + 1, ry + 1, CARD_W - 2, 4)
        pygame.draw.rect(self.display, accent, stripe,
                         border_top_left_radius=6, border_top_right_radius=6)

        # Card name at bottom
        name = card_dict["name"]
        ns   = self.fonts["small"].render(name, True, WHITE if not greyed else MUTED)
        if ns.get_width() > CARD_W - 4:
            ns = pygame.font.Font(None, 16).render(name, True, WHITE if not greyed else MUTED)
        self.display.blit(ns, (rx + CARD_W // 2 - ns.get_width() // 2, ry + CARD_H - 18))

        # Value orb — bottom-left corner
        value = card_dict.get("value", None)
        if value is not None:
            orb_col = MUTED if greyed else accent
            draw_value_orb(self.display, value,
                           rx + 12, ry + CARD_H - 14,
                           orb_col, self.fonts["tiny"], orb_r=11)

        # Stack badge (deck only)
        if in_deck:
            count = self.deck.get(name, 0)
            if count > 1:
                br = pygame.Rect(rx + CARD_W - 26, ry + 5, 22, 18)
                rrect(self.display, (160, 50, 50), br, r=4)
                bt = self.fonts["small"].render(f"×{count}", True, WHITE)
                self.display.blit(bt, (br.x + 1, br.y + 1))

    def draw_scrollbar(self, grid, total_rows):
        r        = grid.clip_rect
        vis_rows = r.height / CARD_CH
        if total_rows <= vis_rows:
            return
        track = pygame.Rect(r.right + 3, r.top, 4, r.height)
        rrect(self.display, PANEL2, track, r=2)
        ratio   = vis_rows / total_rows
        thumb_h = max(20, int(r.height * ratio))
        frac    = grid.scroll_y / max(1, grid._max_scroll)
        thumb_y = r.top + int((r.height - thumb_h) * frac)
        thumb   = pygame.Rect(r.right + 3, thumb_y, 4, thumb_h)
        rrect(self.display, TEAL, thumb, r=2)

    def draw_deck_area(self):
        deck_list = self.expand_deck()
        deck_dicts = [self.card_dict(n) for n in deck_list if self.card_dict(n)]
        self.deck_grid.update_max_scroll(len(deck_dicts))

        panel_r = pygame.Rect(DECK_PANEL_X - PAD, DECK_LABEL_Y - 4,
                              DECK_PANEL_W + PAD + 12, DECK_VIS_H + 34)
        panel(self.display, panel_r, r=10)

        lx, ly = DECK_PANEL_X, DECK_LABEL_Y
        self._txt("DECK", lx, ly, MUTED, "small")
        cc = RED if self.total_cards() >= MAX_DECK else TEAL
        self._txt(f"{self.total_cards()}/{MAX_DECK}", lx + 48, ly, cc, "small")
        if self.unsaved[self.active_deck]:
            self._txt("● unsaved", lx + 110, ly, AMBER, "small")
        if self.deck_grid._max_scroll > 0:
            self._txt("scroll ↕", panel_r.right - 68, ly, DIM, "small")

        self.deck_grid.draw_clip_start()
        for i, cd in enumerate(deck_dicts):
            pos = self.deck_grid.card_pos(i)
            if self.deck_grid.clip_rect.top - CARD_H <= pos[1] <= self.deck_grid.clip_rect.bottom:
                self.draw_card_widget(cd, pos, in_deck=True)
        self.deck_grid.draw_clip_end()

        self.draw_scrollbar(self.deck_grid,
                            max(1, (len(deck_dicts) + CARD_COLS - 1) // CARD_COLS))

    def draw_collection_area(self):
        filt = self.filtered_collection()
        self.coll_grid.update_max_scroll(len(filt))

        panel_r = pygame.Rect(COLL_PANEL_X - PAD, COLL_LABEL_Y - 4,
                              COLL_PANEL_W + PAD + 12, COLL_VIS_H + 34)
        panel(self.display, panel_r, r=10)

        lx, ly = COLL_PANEL_X, COLL_LABEL_Y
        self._txt("COLLECTION", lx, ly, MUTED, "small")
        self._txt(f"{len(filt)}/{len(self.collection)}", lx + 92, ly, MUTED, "small")
        if self.coll_grid._max_scroll > 0:
            self._txt("scroll ↕", panel_r.right - 68, ly, DIM, "small")

        # Category filter pills
        cats = ["All"] + sorted(set(c.get("category","") for c in self.collection if c.get("category")))
        pill_x = lx + 160
        for cat in cats:
            col    = CATEGORY_COLORS.get(cat, BLUE)
            active = (cat == self.active_coll_cat)
            pr     = pygame.Rect(pill_x, ly - 1, max(30, self.fonts["tiny"].size(cat)[0] + 10), 18)
            rrect(self.display, (30, 44, 62) if active else PANEL2, pr, r=4)
            rrect(self.display, col if active else BORDER, pr, r=4, bw=1)
            cs = self.fonts["tiny"].render(cat, True, WHITE if active else MUTED)
            self.display.blit(cs, (pr.x + pr.w // 2 - cs.get_width() // 2,
                                   pr.y + pr.h // 2 - cs.get_height() // 2))
            pill_x += pr.w + 5
        self._coll_cat_pills = list(zip(cats,
            [pygame.Rect(lx + 160 + sum(
                max(30, self.fonts["tiny"].size(c)[0] + 10) + 5 for c in cats[:i]
            ), ly - 1,
            max(30, self.fonts["tiny"].size(cat)[0] + 10), 18)
             for i, cat in enumerate(cats)]))

        self.coll_grid.draw_clip_start()
        for i, cd in enumerate(filt):
            pos   = self.coll_grid.card_pos(i)
            name  = cd["name"]
            avail = self.copies_avail(name)
            owned = self.owned_cards.get(name, 0)
            ind   = self.deck.get(name, 0)
            if self.coll_grid.clip_rect.top - CARD_H <= pos[1] <= self.coll_grid.clip_rect.bottom:
                self.draw_card_widget(cd, pos, in_deck=False, greyed=avail <= 0)
                cc = RED if ind >= owned else MUTED
                ct = self.fonts["small"].render(f"{ind}/{owned}", True, cc)
                self.display.blit(ct, (pos[0] + CARD_W // 2 - ct.get_width() // 2,
                                       pos[1] + CARD_H - 19))
                # Arrow-key selection ring
                if i == self._preview_idx:
                    rrect(self.display, TEAL,
                          pygame.Rect(pos[0], pos[1], CARD_W, CARD_H),
                          r=7, bw=2, bc=TEAL)
        self.coll_grid.draw_clip_end()

        self.draw_scrollbar(self.coll_grid,
                            max(1, (len(filt) + CARD_COLS - 1) // CARD_COLS))

    def draw_tabs(self):
        for i, d in enumerate(DECK_DEFS):
            active = (i == self.active_deck)
            count  = sum(self.decks[i].values())
            label  = f"{d['label']}  {count}"
            rect   = pygame.Rect(550 + i * 200, TABS_Y, 185, TABS_H)
            bg     = (28, 40, 60) if active else PANEL
            bord   = BLUE if active else BORDER
            tc     = WHITE if active else MUTED
            rrect(self.display, bg, rect, r=7)
            rrect(self.display, bord, rect, r=7, bw=2 if active else 1)
            s = self.fonts["normal"].render(label, True, tc)
            self.display.blit(s, (rect.x + 10, rect.y + 12))
            if self.unsaved[i]:
                pygame.draw.circle(self.display, AMBER, (rect.right - 12, rect.top + 9), 4)

    def draw_sidebar(self):
        sx = SIDEBAR_X
        sw = WIDTH - sx + 8
        sr = pygame.Rect(sx - 8, 0, sw, HEIGHT)
        panel(self.display, sr, r=0)

        self._txt("Deck Manager", sx + 6, 18, WHITE, "title")
        self._txt(self.deck_name(), sx + 6, 54, BLUE, "normal")
        pygame.draw.line(self.display, BORDER, (sx, 80), (WIDTH - 4, 80), 1)

        cy          = 90
        preview_w   = sw - 28

        # Card preview
        cy = self.preview.draw_in_sidebar(sx + 6, cy, preview_w)

        # Controls
        controls = [
            ("ESC", "Main menu"),
            ("V",   "Card viewer"),
            ("D",   "Choose deck"),
            ("S",   "Save"),
            ("Z",   "Undo"),
            ("C",   "Clear deck"),
            ("H",   "Hand simulator"),
            ("R",   "Redraw hand"),
            ("SPC", "Draw a card"),
            ("B",   "Back to coll."),
        ]
        for key, desc in controls:
            if cy + 28 > HEIGHT - 10:
                break
            kr = pygame.Rect(sx + 6, cy, 26, 20)
            rrect(self.display, (32, 44, 62), kr, r=4)
            ks = self.fonts["small"].render(key, True, BLUE)
            self.display.blit(ks, (kr.x + kr.w // 2 - ks.get_width() // 2, kr.y + 2))
            self._txt(desc, sx + 38, cy + 2, MUTED, "small")
            cy += 28

        if cy + 10 < HEIGHT:
            pygame.draw.line(self.display, BORDER, (sx, cy + 2), (WIDTH - 4, cy + 2), 1)
            cy += 10

        hints = [("RMB coll.", "add"), ("RMB deck", "remove"), ("Drag", "add/move")]
        for lbl, act in hints:
            if cy + 22 > HEIGHT - 10:
                break
            self._txt(f"{lbl} → {act}", sx + 6, cy, DIM, "small")
            cy += 22

        if cy + 10 < HEIGHT:
            pygame.draw.line(self.display, BORDER, (sx, cy + 2), (WIDTH - 4, cy + 2), 1)
            cy += 10

        if self.hand_sim.active:
            hand_stats = [
                ("Hand",  len(self.hand_sim.hand)),
                ("Pile",  len(self.hand_sim.draw_pile)),
                ("Total", self.total_cards()),
            ]
            for label, val in hand_stats:
                if cy + 20 > HEIGHT - 10: break
                col = TEAL if label == "Hand" else MUTED
                self._txt(f"{label}  {val}", sx + 6, cy, col, "small")
                cy += 20
        else:
         for label, val in [("Unique", len(self.deck)),
                             ("Total",  f"{self.total_cards()}/{MAX_DECK}"),
                             ("Undos",  len(self.undo_stack))]:
             if cy + 20 > HEIGHT - 10:
                 break
             self._txt(f"{label}  {val}", sx + 6, cy, MUTED, "small")
             cy += 20

        if self.status and cy + 10 < HEIGHT:
            pygame.draw.line(self.display, BORDER, (sx, cy + 2), (WIDTH - 4, cy + 2), 1)
            cy += 10
            col = (GREEN if any(w in self.status for w in ("Saved","Added","Loaded","Switched"))
                   else RED   if any(w in self.status for w in ("Full","error","No"))
                   else WHITE)
            self._txt(self.status, sx + 6, cy, col, "normal")

    def draw_drag_ghost(self):
        if not self.dragging_card:
            return
        cd = self.card_dict(self.dragging_card)
        dx = self.drag_pos[0] - CARD_W // 2
        dy = self.drag_pos[1] - CARD_H // 2
        ghost = pygame.Surface((CARD_W, CARD_H), pygame.SRCALPHA)
        pygame.draw.rect(ghost, (*BLUE, 170), (0, 0, CARD_W, CARD_H), border_radius=7)
        pygame.draw.rect(ghost, (*WHITE, 220), (0, 0, CARD_W, CARD_H), 1, border_radius=7)
        self.display.blit(ghost, (dx, dy))
        if cd:
            img = load_card_image(cd["image"], CARD_W - 8, CARD_H - 30)
            self.display.blit(img, (dx + 4, dy + 4))
        s = self.fonts["small"].render(self.dragging_card, True, WHITE)
        self.display.blit(s, (dx + CARD_W // 2 - s.get_width() // 2, dy + CARD_H - 18))

    def _draw_header(self):
        bar = pygame.Rect(0, 0, WIDTH, TABS_Y + TABS_H + 2)
        rrect(self.display, PANEL, bar, r=0)
        pygame.draw.line(self.display, BORDER, (0, bar.bottom), (SIDEBAR_X, bar.bottom), 1)
        self._txt("✦  Deck Builder", 14, TABS_Y + 10, WHITE, "title")
        mode = "HAND MODE" if self.hand_sim.active else self.deck_name().upper()
        col  = TEAL if self.hand_sim.active else BLUE
        self._txt(mode, 220, TABS_Y + 12, col, "small")

    def draw(self):
        self.tick_status()
        self.display.fill(BG)
        self._draw_header()
        self.draw_tabs()
        self.draw_deck_area()
        if self.hand_sim.active:
            self.hand_sim.draw_area(self.draw_card_widget)
        else:
            self.draw_collection_area()
        self.draw_sidebar()
        self.draw_drag_ghost()
        self.selector.draw()


# =====================
# Main
# =====================
def main():
    pygame.init()
    screen  = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Deck Builder")
    clock   = pygame.time.Clock()
    manager = DeckManager(screen)

    running = True
    while running:
        running = manager.handle_events()
        manager.draw()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()