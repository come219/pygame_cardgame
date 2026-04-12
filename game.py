"""
game.py  —  Rock Paper Scissors card game (UI mockup)
Implements the new sidebar / card-preview standard from deck_viewer & card_viewer.
Actual game logic is a placeholder; full implementation comes later.
"""
import pygame
import random
import os

# ─── optional imports for navigation ──────────────────────────────────
try:
    import cardgame as _cardgame
except ImportError:
    _cardgame = None

import cards as _cards_module
ALL_CARDS    = _cards_module.ALL_CARDS
CARD_BY_NAME = {c["name"]: c for c in ALL_CARDS}

# ═════════════════════════════════════════════════════════════════════
# Constants
# ═════════════════════════════════════════════════════════════════════
WIDTH, HEIGHT = 1920, 1080

# ── Palette ───────────────────────────────────────────────────────────
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
FIELD_IDLE    = (28,  36,  50)
FIELD_HOVER   = (34,  52,  42)
FIELD_ACTIVE  = (30,  62,  44)

CATEGORY_COLORS = {
    "Core":    TEAL,
    "Toon":    PURPLE,
    "Special": AMBER,
    "Exodia":  RED,
    "Units":   (75,  175, 120),
    "Spells":  (180, 100, 220),
    "AA":      (220, 140,  60),
}

# ── Layout ────────────────────────────────────────────────────────────
SIDEBAR_X  = 1490
SIDEBAR_W  = WIDTH - SIDEBAR_X
PAD        = 14

CARD_W, CARD_H = 108, 148     # hand / field card size
HAND_Y         = HEIGHT - CARD_H - 30
FIELD_X        = WIDTH  // 2 - 350
FIELD_Y        = HEIGHT // 2 - 180
FIELD_W        = 800
FIELD_H        = 420

# Enemy hand row
ENEMY_HAND_Y   = 60
ENEMY_CARD_W   = 90
ENEMY_CARD_H   = 120

# Deck / graveyard / banished zone positions
DECK_POS      = (1700, 800)
GRAVE_POS     = (1560, 800)
BAN_POS       = (1420, 800)
E_DECK_POS    = (50,   60)
E_GRAVE_POS   = (50,  200)
E_BAN_POS     = (160, 200)

STATUS_DUR = 180

# ═════════════════════════════════════════════════════════════════════
# Helpers
# ═════════════════════════════════════════════════════════════════════
def rrect(surf, color, rect, r=8, bw=0, bc=None):
    pygame.draw.rect(surf, color, rect, border_radius=r)
    if bw and bc:
        pygame.draw.rect(surf, bc, rect, bw, border_radius=r)

def panel(surf, rect, r=10):
    rrect(surf, PANEL, rect, r)
    rrect(surf, BORDER, rect, r, 1)

def clamp(v, lo, hi):
    return max(lo, min(hi, v))

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

def card_accent(card_dict):
    return CATEGORY_COLORS.get(card_dict.get("category", ""), BLUE) if card_dict else BLUE

def draw_value_orb(surf, value, cx, cy, accent, font, orb_r=11):
    pygame.draw.circle(surf, accent, (cx, cy), orb_r)
    pygame.draw.circle(surf, PANEL2,  (cx, cy), orb_r - 3)
    pygame.draw.circle(surf, accent, (cx, cy), orb_r - 6)
    vs = font.render(str(value), True, WHITE)
    surf.blit(vs, (cx - vs.get_width() // 2, cy - vs.get_height() // 2))


# ═════════════════════════════════════════════════════════════════════
# Image cache
# ═════════════════════════════════════════════════════════════════════
_img_cache = {}

def load_img(path, w, h):
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


# ═════════════════════════════════════════════════════════════════════
# Card widget (standalone draw function, no class needed)
# ═════════════════════════════════════════════════════════════════════
def draw_card_tile(surf, fonts, card_dict, rx, ry, w=CARD_W, h=CARD_H,
                   greyed=False, selected=False, face_down=False):
    """Draw a card face-up or face-down at (rx, ry)."""
    mx, my = pygame.mouse.get_pos()
    hov    = rx <= mx <= rx + w and ry <= my <= ry + h and not greyed and not face_down

    if greyed:
        bg, bord = CARD_GREY, (32, 36, 46)
    elif selected:
        bg, bord = CARD_HOV, TEAL
    elif hov:
        bg, bord = CARD_HOV, CARD_BORD_ACT
    else:
        bg, bord = CARD_BG, CARD_BORD

    r = pygame.Rect(rx, ry, w, h)
    rrect(surf, bg, r, r=7)
    rrect(surf, bord, r, r=7, bw=2 if selected else 1)

    if face_down:
        # Card back pattern
        inner = pygame.Rect(rx + 4, ry + 4, w - 8, h - 8)
        rrect(surf, (22, 28, 42), inner, r=5)
        rrect(surf, BORDER, inner, r=5, bw=1)
        # Simple cross-hatch hint
        for i in range(4, w - 4, 12):
            pygame.draw.line(surf, BORDER, (rx + i, ry + 4), (rx + i, ry + h - 4), 1)
        return

    if card_dict is None:
        return

    accent = card_accent(card_dict)

    # Accent stripe
    stripe = pygame.Rect(rx + 1, ry + 1, w - 2, 4)
    pygame.draw.rect(surf, accent, stripe,
                     border_top_left_radius=6, border_top_right_radius=6)

    # Card image
    img_h = h - 28
    img   = load_img(card_dict["image"], w - 4, img_h)
    if greyed:
        gs = img.copy()
        gs.fill((0, 0, 0, 130), special_flags=pygame.BLEND_RGBA_MULT)
        surf.blit(gs, (rx + 2, ry + 6))
    else:
        surf.blit(img, (rx + 2, ry + 6))

    # Name
    name = card_dict["name"]
    ns   = fonts["small"].render(name, True, WHITE if not greyed else MUTED)
    if ns.get_width() > w - 4:
        ns = fonts["tiny"].render(name, True, WHITE if not greyed else MUTED)
    surf.blit(ns, (rx + w // 2 - ns.get_width() // 2, ry + h - 18))

    # Value orb
    value = card_dict.get("value", None)
    if value is not None:
        draw_value_orb(surf, value, rx + 12, ry + h - 14,
                       MUTED if greyed else accent, fonts["tiny"], orb_r=10)


# ═════════════════════════════════════════════════════════════════════
# Sidebar card preview  (ported from deck_viewer)
# ═════════════════════════════════════════════════════════════════════
class CardPreview:
    def __init__(self, display, fonts):
        self.display = display
        self.fonts   = fonts
        self.card    = None
        self.label   = ""    # e.g. "in hand", "on field"

    def set_card(self, card_dict, label=""):
        self.card  = card_dict
        self.label = label

    def draw(self, sx, cy, preview_w):
        """Draw inside sidebar starting at (sx, cy). Returns new cy."""
        fs = self.fonts["small"]
        fn = self.fonts["normal"]
        fl = self.fonts["large"]
        fd = self.fonts["desc"]

        if self.card is None:
            t  = fs.render("Hover a card", True, MUTED)
            t2 = fs.render("to preview it", True, DIM)
            self.display.blit(t,  (sx + preview_w // 2 - t.get_width()  // 2, cy + 8))
            self.display.blit(t2, (sx + preview_w // 2 - t2.get_width() // 2, cy + 26))
            return cy + 50

        accent = card_accent(self.card)

        # Accent bar
        pygame.draw.rect(self.display, accent,
                         pygame.Rect(sx, cy, preview_w, 5),
                         border_top_left_radius=6, border_top_right_radius=6)
        cy += 7

        # Image
        iw = preview_w - 4
        ih = int(iw * 0.9)
        img = load_img(self.card["image"], iw, ih)
        self.display.blit(img, (sx + 2, cy))
        cy += ih + 6

        # Name
        ns = fl.render(self.card["name"], True, WHITE)
        if ns.get_width() > preview_w:
            ns = fn.render(self.card["name"], True, WHITE)
        self.display.blit(ns, (sx + preview_w // 2 - ns.get_width() // 2, cy))
        cy += ns.get_height() + 4

        # Category
        cat_s = fs.render(self.card.get("category", "").upper(), True, accent)
        self.display.blit(cat_s, (sx + preview_w // 2 - cat_s.get_width() // 2, cy))
        cy += cat_s.get_height() + 6

        # Value orb
        value = self.card.get("value", None)
        if value is not None:
            orb_r  = 18
            orb_cx = sx + preview_w // 2
            orb_cy = cy + orb_r
            pygame.draw.circle(self.display, accent, (orb_cx, orb_cy), orb_r)
            pygame.draw.circle(self.display, PANEL2,  (orb_cx, orb_cy), orb_r - 3)
            pygame.draw.circle(self.display, accent, (orb_cx, orb_cy), orb_r - 7)
            vs = fn.render(str(value), True, WHITE)
            self.display.blit(vs, (orb_cx - vs.get_width() // 2, orb_cy - vs.get_height() // 2))
            cy += orb_r * 2 + 8

        # Label (in hand / on field)
        if self.label:
            lt = fs.render(self.label, True, TEAL)
            self.display.blit(lt, (sx + preview_w // 2 - lt.get_width() // 2, cy))
            cy += lt.get_height() + 4

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

        pygame.draw.line(self.display, BORDER, (sx + 4, cy), (sx + preview_w - 4, cy), 1)
        cy += 8
        return cy


# ═════════════════════════════════════════════════════════════════════
# Zone widgets  (deck pile, graveyard, banished)
# ═════════════════════════════════════════════════════════════════════
class ZonePile:
    """A face-down deck pile or face-up graveyard / banished zone."""
    def __init__(self, label, pos, img_path, color=MUTED, face_down=True):
        self.label     = label
        self.pos       = pos
        self.color     = color
        self.face_down = face_down
        self.cards     = []
        self._img      = load_img(img_path, 80, 80) if os.path.exists(img_path) else None
        self.rect      = pygame.Rect(pos[0], pos[1], 80, 100)

    def draw(self, surf, fonts):
        x, y = self.pos
        rrect(surf, PANEL, self.rect, r=6)
        rrect(surf, self.color, self.rect, r=6, bw=1)
        if self._img:
            surf.blit(self._img, (x, y + 10))
        else:
            t = fonts["tiny"].render(self.label[0], True, self.color)
            surf.blit(t, (x + 40 - t.get_width() // 2, y + 36))
        # count badge
        count_s = fonts["small"].render(f"{self.label}:{len(self.cards)}", True, self.color)
        surf.blit(count_s, (x, y + 86))

    def hovered(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())


# ═════════════════════════════════════════════════════════════════════
# Main game class
# ═════════════════════════════════════════════════════════════════════
class Game:
    HAND_SIZE    = 5
    DOUBLE_CLICK = 400   # ms

    # Starting deck — names that must exist in ALL_CARDS
    STARTING_DECK = [
        "Rock", "Rock", "Paper", "Paper",
        "Scissors", "Scissors", "Fire", "Water", "Wind",
        "Knight", "Archer", "Mage",
    ]

    def __init__(self, display):
        self.display = display

        self.fonts = {
            "normal": pygame.font.Font(None, 26),
            "small":  pygame.font.Font(None, 21),
            "large":  pygame.font.Font(None, 42),
            "title":  pygame.font.Font(None, 34),
            "desc":   pygame.font.Font(None, 20),
            "tiny":   pygame.font.Font(None, 17),
        }

        # ── Player state ──────────────────────────────────────────────
        self.player_deck      = [c for c in self.STARTING_DECK if c in CARD_BY_NAME]
        random.shuffle(self.player_deck)
        self.player_hand      = []
        self.player_field     = []      # max 2 for now
        self.player_graveyard = []
        self.player_banished  = []
        self.player_hp        = 20

        # ── Enemy state ───────────────────────────────────────────────
        self.enemy_deck      = [c for c in self.STARTING_DECK if c in CARD_BY_NAME]
        random.shuffle(self.enemy_deck)
        self.enemy_hand      = []        # face-down
        self.enemy_field     = []
        self.enemy_graveyard = []
        self.enemy_banished  = []
        self.enemy_hp        = 20

        # ── UI state ──────────────────────────────────────────────────
        self.selected_hand_idx  = -1     # which hand card is selected
        self.dragging           = False
        self.drag_card_name     = None
        self.drag_origin        = None   # "hand" or "field"
        self.drag_pos           = (0, 0)

        self.status        = ""
        self.status_timer  = 0
        self.round         = 1
        self.phase         = "draw"      # draw → main → battle → end
        self.result        = None        # "Player Wins" / "Enemy Wins" / "Draw"

        self.show_graveyard = False
        self.show_banished  = False
        self.show_history   = False
        self.history_log    = []

        self.last_click_time = 0

        # ── Preview sidebar ───────────────────────────────────────────
        self.preview = CardPreview(display, self.fonts)

        # ── Zone piles ────────────────────────────────────────────────
        self.p_deck   = ZonePile("Deck",    DECK_POS,  "assets/deck_image.png",       BLUE,  True)
        self.p_grave  = ZonePile("Grave",   GRAVE_POS, "assets/graveyard_image.png",  MUTED, False)
        self.p_ban    = ZonePile("Banish",  BAN_POS,   "assets/banished_icon.png",    AMBER, False)
        self.e_deck   = ZonePile("Deck",    E_DECK_POS,  "assets/deck_image.png",     RED,   True)
        self.e_grave  = ZonePile("Grave",   E_GRAVE_POS, "assets/graveyard_image.png",MUTED, False)
        self.e_ban    = ZonePile("Banish",  E_BAN_POS,   "assets/banished_icon.png",  AMBER, False)

        # ── Initial draw ──────────────────────────────────────────────
        self._draw_cards(self.HAND_SIZE)
        self._enemy_draw(self.HAND_SIZE)
        self._log("Round 1 started")
        self._log(f"Player draws {self.HAND_SIZE} cards")
        self._log(f"Enemy draws {self.HAND_SIZE} cards")

    # ─── helpers ──────────────────────────────────────────────────────
    def _txt(self, text, x, y, color=WHITE, fk="normal"):
        s = self.fonts[fk].render(text, True, color)
        self.display.blit(s, (x, y))

    def set_status(self, msg):
        self.status       = msg
        self.status_timer = STATUS_DUR

    def tick_status(self):
        if self.status_timer > 0:
            self.status_timer -= 1
            if self.status_timer == 0:
                self.status = ""

    def _log(self, msg):
        self.history_log.append(msg)
        if len(self.history_log) > 30:
            self.history_log.pop(0)

    def _draw_cards(self, n=1):
        for _ in range(n):
            if self.player_deck:
                self.player_hand.append(self.player_deck.pop())

    def _enemy_draw(self, n=1):
        for _ in range(n):
            if self.enemy_deck:
                self.enemy_hand.append(self.enemy_deck.pop())

    def _hand_card_rect(self, idx):
        total   = len(self.player_hand)
        spacing = min(CARD_W + 10, (SIDEBAR_X - 80) // max(1, total))
        start_x = (SIDEBAR_X - total * spacing) // 2
        return pygame.Rect(start_x + idx * spacing, HAND_Y, CARD_W, CARD_H)

    def _field_slot_rect(self, idx):
        """Two player field slots side by side."""
        return pygame.Rect(FIELD_X + 30 + idx * (CARD_W + 20), FIELD_Y + FIELD_H // 2 + 10,
                           CARD_W, CARD_H)

    def _enemy_field_slot_rect(self, idx):
        return pygame.Rect(FIELD_X + 30 + idx * (CARD_W + 20), FIELD_Y + 20,
                           CARD_W, CARD_H)

    def _card_at_hand(self, pos):
        for i in range(len(self.player_hand)):
            if self._hand_card_rect(i).collidepoint(pos):
                return i
        return -1

    def _card_at_field(self, pos):
        for i in range(len(self.player_field)):
            if self._field_slot_rect(i).collidepoint(pos):
                return i
        return -1

    def _in_field_zone(self, pos):
        return pygame.Rect(FIELD_X, FIELD_Y, FIELD_W, FIELD_H).collidepoint(pos)

    def _play_to_field(self, hand_idx):
        if len(self.player_field) >= 2:
            self.set_status("Field full! (max 2)")
            return
        name = self.player_hand.pop(hand_idx)
        self.player_field.append(name)
        self.selected_hand_idx = -1
        self._log(f"Player played {name}")
        self.set_status(f"Played {name}")
        self.preview.set_card(CARD_BY_NAME.get(name), "on field")

    def _resolve_battle(self):
        """Simple RPS resolution — placeholder for full logic."""
        BEATS = {
            "Rock": ["Scissors"], "Paper": ["Rock"], "Scissors": ["Paper"],
            "Fire": ["Wind", "Ice"], "Water": ["Fire"], "Wind": ["Earth"],
            "Earth": ["Water", "Lightning"], "Lightning": ["Water"],
            "Ice": ["Wind"], "Shadow": ["Light"], "Light": ["Shadow"],
        }

        p_names = self.player_field[:]
        e_names = self.enemy_field[:] if self.enemy_field else [random.choice(
            ["Rock","Paper","Scissors"])]

        wins = 0
        for pn in p_names:
            for en in e_names:
                if en in BEATS.get(pn, []):
                    wins += 1

        if wins > 0:
            self.result = "Player Wins"
            self.enemy_hp = max(0, self.enemy_hp - wins)
            self._log(f"Player wins the round! (+{wins} damage)")
        elif not p_names:
            self.result = "Enemy Wins"
            self.player_hp = max(0, self.player_hp - 1)
            self._log("Enemy wins (no cards played)")
        else:
            self.result = "Draw"
            self._log("Round draws")

        # Move field to graveyard
        self.player_graveyard.extend(self.player_field)
        self.enemy_graveyard.extend(self.enemy_field)
        self.player_field.clear()
        self.enemy_field.clear()
        self.set_status(f"Result: {self.result}")

    def _end_turn(self):
        # Enemy plays a random card
        if self.enemy_hand:
            played = random.choice(self.enemy_hand)
            self.enemy_hand.remove(played)
            self.enemy_field.append(played)
            self._log(f"Enemy plays a card")

        self._resolve_battle()
        self.round += 1
        self.phase = "draw"

        # Refill hands
        if len(self.player_hand) < self.HAND_SIZE and self.player_deck:
            drawn = min(2, self.HAND_SIZE - len(self.player_hand))
            self._draw_cards(drawn)
            self._log(f"Player draws {drawn}")
        if len(self.enemy_hand) < self.HAND_SIZE and self.enemy_deck:
            self._enemy_draw(min(2, self.HAND_SIZE - len(self.enemy_hand)))

        self.p_deck.cards   = self.player_deck
        self.p_grave.cards  = self.player_graveyard
        self.p_ban.cards    = self.player_banished
        self.e_deck.cards   = self.enemy_deck
        self.e_grave.cards  = self.enemy_graveyard
        self.e_ban.cards    = self.enemy_banished

    # ═════════════════════════════════════════════════════════════════
    # Event handling
    # ═════════════════════════════════════════════════════════════════
    def handle_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return False

            elif e.type == pygame.MOUSEMOTION:
                self.drag_pos = e.pos
                self._hover_update(e.pos)

            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                self._on_click(e.pos)

            elif e.type == pygame.MOUSEBUTTONUP and e.button == 1:
                self._on_release(e.pos)

            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    if _cardgame:
                        _cardgame.main()
                    return False
                elif e.key == pygame.K_e:
                    self._end_turn()
                elif e.key == pygame.K_d:
                    self._draw_cards(1)
                    self.set_status("Drew a card")
                elif e.key == pygame.K_r:
                    self.player_field.clear()
                    self.selected_hand_idx = -1
                    self.set_status("Field cleared")
                elif e.key == pygame.K_h:
                    self.show_history  = not self.show_history
                    self.show_graveyard = False
                    self.show_banished  = False
                elif e.key == pygame.K_g:
                    self.show_graveyard = not self.show_graveyard
                    self.show_history   = False
                    self.show_banished  = False
                elif e.key == pygame.K_b:
                    self.show_banished  = not self.show_banished
                    self.show_history   = False
                    self.show_graveyard = False

        return True

    def _hover_update(self, pos):
        """Update preview on hover."""
        # Hand cards
        for i in range(len(self.player_hand)):
            if self._hand_card_rect(i).collidepoint(pos):
                name = self.player_hand[i]
                self.preview.set_card(CARD_BY_NAME.get(name), "in hand")
                return
        # Field cards
        for i in range(len(self.player_field)):
            if self._field_slot_rect(i).collidepoint(pos):
                name = self.player_field[i]
                self.preview.set_card(CARD_BY_NAME.get(name), "on field")
                return
        # Enemy field (revealed after battle)
        for i in range(len(self.enemy_field)):
            if self._enemy_field_slot_rect(i).collidepoint(pos):
                name = self.enemy_field[i]
                self.preview.set_card(CARD_BY_NAME.get(name), "enemy field")
                return

    def _on_click(self, pos):
        now = pygame.time.get_ticks()
        double = (now - self.last_click_time) <= self.DOUBLE_CLICK
        self.last_click_time = now

        # Double-click hand card → play to field
        if double:
            idx = self._card_at_hand(pos)
            if idx >= 0:
                self._play_to_field(idx)
                return

        # Single-click hand card → select / start drag
        idx = self._card_at_hand(pos)
        if idx >= 0:
            self.selected_hand_idx = idx
            self.dragging          = True
            self.drag_card_name    = self.player_hand[idx]
            self.drag_origin       = "hand"
            name = self.player_hand[idx]
            self.preview.set_card(CARD_BY_NAME.get(name), "in hand")
            return

        # Click on field card → select for info
        idx = self._card_at_field(pos)
        if idx >= 0:
            name = self.player_field[idx]
            self.preview.set_card(CARD_BY_NAME.get(name), "on field")
            return

        # End-turn button
        if pygame.Rect(WIDTH - 180, HEIGHT - 60, 160, 44).collidepoint(pos):
            self._end_turn()

        # Draw button
        if pygame.Rect(WIDTH - 360, HEIGHT - 60, 160, 44).collidepoint(pos):
            self._draw_cards(1)
            self.set_status("Drew a card")

    def _on_release(self, pos):
        if self.dragging and self.drag_card_name:
            # Dropped in field zone → play card
            if self._in_field_zone(pos) and self.drag_origin == "hand":
                idx = self.player_hand.index(self.drag_card_name) if self.drag_card_name in self.player_hand else -1
                if idx >= 0:
                    self._play_to_field(idx)
        self.dragging       = False
        self.drag_card_name = None
        self.drag_origin    = None

    # ═════════════════════════════════════════════════════════════════
    # Drawing
    # ═════════════════════════════════════════════════════════════════
    def _draw_header(self):
        bar = pygame.Rect(0, 0, SIDEBAR_X, 52)
        rrect(self.display, PANEL, bar, r=0)
        pygame.draw.line(self.display, BORDER, (0, 52), (SIDEBAR_X, 52), 1)
        self._txt("✦  Card Duel", 16, 12, WHITE, "title")
        phase_col = {
            "draw": TEAL, "main": BLUE, "battle": RED, "end": AMBER
        }.get(self.phase, MUTED)
        self._txt(f"Phase: {self.phase.upper()}", 220, 14, phase_col, "small")
        self._txt(f"Round {self.round}", 380, 14, MUTED, "small")

    def _draw_field(self):
        # Field background
        fr = pygame.Rect(FIELD_X, FIELD_Y, FIELD_W, FIELD_H)
        mouse_in = fr.collidepoint(pygame.mouse.get_pos()) and self.dragging
        rrect(self.display, FIELD_ACTIVE if mouse_in else FIELD_IDLE, fr, r=10)
        rrect(self.display, TEAL if mouse_in else BORDER, fr, r=10, bw=2 if mouse_in else 1)

        # Divider line
        mid_y = FIELD_Y + FIELD_H // 2
        pygame.draw.line(self.display, BORDER, (FIELD_X + 10, mid_y), (FIELD_X + FIELD_W - 10, mid_y), 1)

        # Labels
        self._txt("ENEMY FIELD", FIELD_X + 8, FIELD_Y + 6, DIM, "tiny")
        self._txt("PLAYER FIELD", FIELD_X + 8, mid_y + 6, DIM, "tiny")

        # Empty slot outlines
        for i in range(2):
            sr = self._field_slot_rect(i)
            if i >= len(self.player_field):
                rrect(self.display, PANEL2, sr, r=6)
                rrect(self.display, BORDER, sr, r=6, bw=1)
                ph = self.fonts["tiny"].render("drop here", True, DIM)
                self.display.blit(ph, (sr.centerx - ph.get_width() // 2, sr.centery - 6))

            er = self._enemy_field_slot_rect(i)
            if i >= len(self.enemy_field):
                rrect(self.display, PANEL2, er, r=6)
                rrect(self.display, BORDER, er, r=6, bw=1)

        # Player field cards
        for i, name in enumerate(self.player_field):
            sr = self._field_slot_rect(i)
            draw_card_tile(self.display, self.fonts, CARD_BY_NAME.get(name),
                           sr.x, sr.y, CARD_W, CARD_H)

        # Enemy field cards (face-down unless result revealed)
        for i, name in enumerate(self.enemy_field):
            er = self._enemy_field_slot_rect(i)
            revealed = (self.result is not None)
            draw_card_tile(self.display, self.fonts, CARD_BY_NAME.get(name),
                           er.x, er.y, CARD_W, CARD_H,
                           face_down=not revealed)

    def _draw_hand(self):
        # Panel behind hand
        hand_panel = pygame.Rect(0, HAND_Y - 14, SIDEBAR_X, CARD_H + 28)
        panel(self.display, hand_panel, r=0)

        self._txt(f"Hand ({len(self.player_hand)})", PAD, HAND_Y - 12, MUTED, "small")

        for i in range(len(self.player_hand)):
            r    = self._hand_card_rect(i)
            name = self.player_hand[i]
            sel  = (i == self.selected_hand_idx)
            # Lift selected card slightly
            y_off = -8 if sel else 0
            draw_card_tile(self.display, self.fonts, CARD_BY_NAME.get(name),
                           r.x, r.y + y_off, CARD_W, CARD_H, selected=sel)

    def _draw_enemy_hand(self):
        """Draw enemy hand as face-down cards."""
        n       = len(self.enemy_hand)
        spacing = min(ENEMY_CARD_W + 8, (SIDEBAR_X // 2) // max(1, n))
        start_x = FIELD_X + FIELD_W + 20
        for i in range(n):
            draw_card_tile(self.display, self.fonts, None,
                           start_x + i * spacing, ENEMY_HAND_Y,
                           ENEMY_CARD_W, ENEMY_CARD_H, face_down=True)
        self._txt(f"Enemy hand: {n}", start_x, ENEMY_HAND_Y + ENEMY_CARD_H + 4, DIM, "tiny")

    def _draw_hp_bars(self):
        # Player HP
        px, py = PAD, HEIGHT - 58
        self._txt(f"Player HP: {self.player_hp}", px, py, GREEN if self.player_hp > 10 else RED, "normal")
        bar_bg = pygame.Rect(px, py + 22, 200, 8)
        rrect(self.display, PANEL2, bar_bg, r=4)
        fill_w = int(200 * max(0, self.player_hp) / 20)
        rrect(self.display, GREEN if self.player_hp > 10 else RED,
              pygame.Rect(px, py + 22, fill_w, 8), r=4)

        # Enemy HP
        ex, ey = PAD, 56
        self._txt(f"Enemy HP: {self.enemy_hp}", ex, ey, RED if self.enemy_hp <= 10 else MUTED, "normal")
        bar_bg2 = pygame.Rect(ex, ey + 22, 200, 8)
        rrect(self.display, PANEL2, bar_bg2, r=4)
        fill_w2 = int(200 * max(0, self.enemy_hp) / 20)
        rrect(self.display, RED if self.enemy_hp <= 10 else MUTED,
              pygame.Rect(ex, ey + 22, fill_w2, 8), r=4)

    def _draw_zones(self):
        self.p_deck.cards  = self.player_deck
        self.p_grave.cards = self.player_graveyard
        self.p_ban.cards   = self.player_banished
        self.e_deck.cards  = self.enemy_deck
        self.e_grave.cards = self.enemy_graveyard
        self.e_ban.cards   = self.enemy_banished

        for zone in (self.p_deck, self.p_grave, self.p_ban,
                     self.e_deck, self.e_grave, self.e_ban):
            zone.draw(self.display, self.fonts)

    def _draw_buttons(self):
        bw, bh = 160, 44
        # Draw button
        dr = pygame.Rect(SIDEBAR_X - 370, HEIGHT - 60, bw, bh)
        hd = dr.collidepoint(pygame.mouse.get_pos())
        rrect(self.display, (30, 44, 62) if hd else PANEL2, dr, r=8)
        rrect(self.display, TEAL if hd else BORDER, dr, r=8, bw=1)
        dt = self.fonts["normal"].render("D  Draw", True, TEAL if hd else MUTED)
        self.display.blit(dt, (dr.centerx - dt.get_width() // 2, dr.centery - dt.get_height() // 2))

        # End Turn button
        er = pygame.Rect(SIDEBAR_X - 190, HEIGHT - 60, bw, bh)
        he = er.collidepoint(pygame.mouse.get_pos())
        rrect(self.display, (44, 28, 28) if he else PANEL2, er, r=8)
        rrect(self.display, RED if he else BORDER, er, r=8, bw=1)
        et = self.fonts["normal"].render("E  End Turn", True, RED if he else MUTED)
        self.display.blit(et, (er.centerx - et.get_width() // 2, er.centery - et.get_height() // 2))

    def _draw_result_banner(self):
        if not self.result:
            return
        col = GREEN if self.result == "Player Wins" else RED if self.result == "Enemy Wins" else AMBER
        t   = self.fonts["large"].render(self.result, True, col)
        bx  = WIDTH // 2 - t.get_width() // 2 - 20
        br  = pygame.Rect(bx, FIELD_Y + FIELD_H // 2 - 26, t.get_width() + 40, 52)
        rrect(self.display, PANEL2, br, r=10)
        rrect(self.display, col, br, r=10, bw=2)
        self.display.blit(t, (bx + 20, FIELD_Y + FIELD_H // 2 - t.get_height() // 2))

    def _draw_overlay(self, title, lines):
        ox = WIDTH // 4
        oy = HEIGHT // 4
        ow = WIDTH // 2
        oh = HEIGHT // 2
        rrect(self.display, PANEL2, pygame.Rect(ox, oy, ow, oh), r=12)
        rrect(self.display, BORDER, pygame.Rect(ox, oy, ow, oh), r=12, bw=1)
        tl = self.fonts["title"].render(title, True, WHITE)
        self.display.blit(tl, (ox + ow // 2 - tl.get_width() // 2, oy + 16))
        for i, line in enumerate(lines[-18:]):
            lt = self.fonts["small"].render(line, True, MUTED)
            self.display.blit(lt, (ox + 20, oy + 52 + i * 22))

    def _draw_sidebar(self):
        sx = SIDEBAR_X
        sw = WIDTH - sx
        panel(self.display, pygame.Rect(sx - 8, 0, sw + 8, HEIGHT), r=0)

        self._txt("Card Duel", sx + 6, 18, WHITE, "title")
        phase_col = {
            "draw": TEAL, "main": BLUE, "battle": RED, "end": AMBER
        }.get(self.phase, MUTED)
        self._txt(self.phase.upper(), sx + 6, 54, phase_col, "small")
        pygame.draw.line(self.display, BORDER, (sx, 78), (WIDTH - 4, 78), 1)

        cy       = 88
        prev_w   = sw - 20

        # Card preview
        cy = self.preview.draw(sx + 6, cy, prev_w)

        # Controls
        controls = [
            ("ESC", "Main menu"),
            ("E",   "End turn"),
            ("D",   "Draw card"),
            ("R",   "Reset field"),
            ("H",   "History log"),
            ("G",   "Graveyard"),
            ("B",   "Banished"),
        ]
        for key, desc in controls:
            if cy + 28 > HEIGHT - 10: break
            kr = pygame.Rect(sx + 6, cy, 26, 20)
            rrect(self.display, (32, 44, 62), kr, r=4)
            ks = self.fonts["small"].render(key, True, BLUE)
            self.display.blit(ks, (kr.centerx - ks.get_width() // 2, kr.y + 2))
            self._txt(desc, sx + 38, cy + 2, MUTED, "small")
            cy += 28

        pygame.draw.line(self.display, BORDER, (sx, cy + 2), (WIDTH - 4, cy + 2), 1)
        cy += 10

        hints = [("Dbl-click", "play card"), ("Drag", "play to field")]
        for lbl, act in hints:
            if cy + 22 > HEIGHT - 10: break
            self._txt(f"{lbl} → {act}", sx + 6, cy, DIM, "small")
            cy += 22

        pygame.draw.line(self.display, BORDER, (sx, cy + 2), (WIDTH - 4, cy + 2), 1)
        cy += 10

        stats = [
            ("Player HP", self.player_hp),
            ("Enemy HP",  self.enemy_hp),
            ("Deck left", len(self.player_deck)),
            ("Hand",      len(self.player_hand)),
            ("Graveyard", len(self.player_graveyard)),
        ]
        for lbl, val in stats:
            if cy + 20 > HEIGHT - 10: break
            col = RED if lbl == "Enemy HP" and self.enemy_hp <= 5 else \
                  GREEN if lbl == "Player HP" and self.player_hp > 10 else MUTED
            self._txt(f"{lbl}  {val}", sx + 6, cy, col, "small")
            cy += 20

        if self.status and cy + 10 < HEIGHT:
            pygame.draw.line(self.display, BORDER, (sx, cy + 2), (WIDTH - 4, cy + 2), 1)
            cy += 10
            col = (GREEN if any(w in self.status for w in ("Wins","Drew","Played"))
                   else RED   if any(w in self.status for w in ("full","Empty","Wins Enemy"))
                   else WHITE)
            self._txt(self.status, sx + 6, cy, col, "normal")

    def _draw_drag_ghost(self):
        if not self.dragging or not self.drag_card_name:
            return
        cd = CARD_BY_NAME.get(self.drag_card_name)
        dx = self.drag_pos[0] - CARD_W // 2
        dy = self.drag_pos[1] - CARD_H // 2
        ghost = pygame.Surface((CARD_W, CARD_H), pygame.SRCALPHA)
        pygame.draw.rect(ghost, (*BLUE, 150), (0, 0, CARD_W, CARD_H), border_radius=7)
        pygame.draw.rect(ghost, (*WHITE, 200), (0, 0, CARD_W, CARD_H), 1, border_radius=7)
        self.display.blit(ghost, (dx, dy))
        if cd:
            img = load_img(cd["image"], CARD_W - 8, CARD_H - 28)
            self.display.blit(img, (dx + 4, dy + 4))
        ns = self.fonts["small"].render(self.drag_card_name, True, WHITE)
        self.display.blit(ns, (dx + CARD_W // 2 - ns.get_width() // 2, dy + CARD_H - 18))

    def draw(self):
        self.tick_status()
        self.display.fill(BG)

        self._draw_header()
        self._draw_hp_bars()
        self._draw_field()
        self._draw_enemy_hand()
        self._draw_zones()
        self._draw_hand()
        self._draw_buttons()
        self._draw_result_banner()
        self._draw_sidebar()
        self._draw_drag_ghost()

        # Overlays (history / graveyard / banished)
        if self.show_history:
            self._draw_overlay("History Log", self.history_log)
        elif self.show_graveyard:
            items = [f"{i+1}. {n}" for i, n in enumerate(self.player_graveyard)] or ["(empty)"]
            self._draw_overlay("Player Graveyard", items)
        elif self.show_banished:
            items = [f"{i+1}. {n}" for i, n in enumerate(self.player_banished)] or ["(empty)"]
            self._draw_overlay("Player Banished", items)


# ═════════════════════════════════════════════════════════════════════
# Entry point
# ═════════════════════════════════════════════════════════════════════
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Card Duel")
    clock  = pygame.time.Clock()
    game   = Game(screen)

    running = True
    while running:
        running = game.handle_events()
        game.draw()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()