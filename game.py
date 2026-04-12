"""
game.py  —  Card Duel (UI + logic mockup)
Sidebar / card-preview / value orbs match deck_viewer & card_viewer standards.
"""
import pygame, random, os, math

try:
    import cardgame as _cardgame
except ImportError:
    _cardgame = None

import cards as _cards_module
ALL_CARDS    = _cards_module.ALL_CARDS
CARD_BY_NAME = {c["name"]: c for c in ALL_CARDS}

# ══════════════════════════════════════════════════════════════════════
# Constants & palette
# ══════════════════════════════════════════════════════════════════════
WIDTH, HEIGHT  = 1920, 1080

BG            = (12,  14,  20)
PANEL         = (20,  24,  34)
PANEL2        = (26,  30,  42)
PANEL3        = (32,  38,  54)
BORDER        = (38,  46,  64)
BORDER_HI     = (60,  80, 120)
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
OVERLAY_COL   = (8,   10,  16, 230)

FIELD_IDLE    = (22,  32,  44)
FIELD_HOVER   = (28,  50,  38)
FIELD_ACTIVE  = (24,  58,  40)
FIELD_SEP     = (34,  44,  62)

ENEMY_BG      = (22,  14,  22)

CATEGORY_COLORS = {
    "Core":    TEAL,   "Toon":   PURPLE, "Special": AMBER,
    "Exodia":  RED,    "Units":  (75, 175, 120),
    "Spells":  (180, 100, 220), "AA": (220, 140, 60),
}

# ── Layout ────────────────────────────────────────────────────────────
SIDEBAR_X  = 1490
PAD        = 14

CARD_W, CARD_H      = 118, 162     # field / hand cards
HAND_Y              = HEIGHT - CARD_H - 36

FIELD_X, FIELD_Y    = 380, 340
FIELD_W, FIELD_H    = 900, 440
FIELD_SLOTS         = 3            # slots per side
FIELD_SLOT_W        = CARD_W + 18

E_CARD_W, E_CARD_H  = 88, 120      # enemy hand (face-down)
E_HAND_Y            = 56

ZONE_W, ZONE_H      = 86, 110

DECK_POS    = (PAD, 820)
GRAVE_POS   = (PAD, 690)
BAN_POS     = (PAD + 100, 690)
E_DECK_POS  = (PAD,       190)
E_GRAVE_POS = (PAD,      330)
E_BAN_POS   = (PAD + 100 , 330)

STATUS_DUR  = 200
MAX_HP      = 20

STARTING_DECK = [
    "Rock","Rock","Paper","Paper","Scissors","Scissors",
    "Fire","Water","Wind","Earth","Lightning","Ice",
    "Knight","Archer","Mage","Dragon","Goblin","Shield",
]

BEATS = {
    "Rock":["Scissors","Goblin"],  "Paper":["Rock","Shield"],
    "Scissors":["Paper","Mage"],   "Fire":["Wind","Ice","Goblin"],
    "Water":["Fire","Earth"],      "Wind":["Earth","Archer"],
    "Earth":["Lightning","Water"], "Lightning":["Water","Knight"],
    "Ice":["Wind","Dragon"],       "Shadow":["Light","Mage"],
    "Light":["Shadow","Goblin"],   "Void":["Light","Shield"],
    "Dragon":["Knight","Mage"],    "Goblin":["Archer","Shield"],
    "Knight":["Goblin","Archer"],  "Archer":["Mage","Shield"],
    "Mage":["Dragon","Knight"],    "Shield":["Fire","Lightning"],
}



# ══════════════════════════════════════════════════════════════════════
# Helpers
# ══════════════════════════════════════════════════════════════════════
def rrect(surf, color, rect, r=8, bw=0, bc=None):
    pygame.draw.rect(surf, color, rect, border_radius=r)
    if bw and bc:
        pygame.draw.rect(surf, bc, rect, bw, border_radius=r)

def panel(surf, rect, r=10):
    rrect(surf, PANEL, rect, r)
    rrect(surf, BORDER, rect, r, 1)

def clamp(v, lo, hi): return max(lo, min(hi, v))

def lerp_color(a, b, t):
    return tuple(int(a[i] + (b[i]-a[i])*t) for i in range(3))

def wrap_text(font, text, max_w):
    words, lines, line = text.split(), [], ""
    for w in words:
        test = (line+" "+w).strip()
        if font.size(test)[0] <= max_w: line = test
        else:
            if line: lines.append(line)
            line = w
    if line: lines.append(line)
    return lines

def card_accent(cd):
    return CATEGORY_COLORS.get(cd.get("category",""), BLUE) if cd else BLUE

def draw_value_orb(surf, value, cx, cy, accent, font, orb_r=11):
    pygame.draw.circle(surf, accent, (cx, cy), orb_r)
    pygame.draw.circle(surf, PANEL2,  (cx, cy), orb_r-3)
    pygame.draw.circle(surf, accent, (cx, cy), orb_r-6)
    vs = font.render(str(value), True, WHITE)
    surf.blit(vs, (cx-vs.get_width()//2, cy-vs.get_height()//2))

# ══════════════════════════════════════════════════════════════════════
# Image / sound cache
# ══════════════════════════════════════════════════════════════════════
_img_cache = {}
def load_img(path, w, h):
    key = (path, w, h)
    if key in _img_cache: return _img_cache[key]
    try:
        img = pygame.image.load(path).convert_alpha()
        img = pygame.transform.smoothscale(img, (w, h))
    except Exception:
        img = pygame.Surface((w, h), pygame.SRCALPHA)
        img.fill((38, 44, 60, 200))
    _img_cache[key] = img
    return img

# ══════════════════════════════════════════════════════════════════════
# Floating text / particle system
# ══════════════════════════════════════════════════════════════════════
class FloatText:
    def __init__(self, text, x, y, color=WHITE, size=28, life=90):
        self.text  = text
        self.x     = float(x)
        self.y     = float(y)
        self.color = color
        self.life  = life
        self.max   = life
        self.vy    = -1.4
        self.font  = pygame.font.Font(None, size)

    def update(self):
        self.y   += self.vy
        self.vy  *= 0.97
        self.life -= 1

    def draw(self, surf):
        alpha = int(255 * self.life / self.max)
        s = self.font.render(self.text, True, self.color)
        s.set_alpha(alpha)
        surf.blit(s, (int(self.x) - s.get_width()//2, int(self.y)))

    @property
    def alive(self): return self.life > 0

# ══════════════════════════════════════════════════════════════════════
# Card tile renderer
# ══════════════════════════════════════════════════════════════════════
def draw_card_tile(surf, fonts, cd, rx, ry, w=CARD_W, h=CARD_H,
                   greyed=False, selected=False, face_down=False,
                   glowing=False, played=False):
    mx, my = pygame.mouse.get_pos()
    hov    = rx<=mx<=rx+w and ry<=my<=ry+h and not greyed and not face_down

    if greyed:    bg, bord = CARD_GREY, (32,36,46)
    elif selected: bg, bord = CARD_HOV,  TEAL
    elif glowing:  bg, bord = (40,56,48), GREEN
    elif hov:     bg, bord = CARD_HOV,  CARD_BORD_ACT
    else:         bg, bord = CARD_BG,   CARD_BORD

    r = pygame.Rect(rx, ry, w, h)
    rrect(surf, bg, r, r=8)
    bw = 2 if (selected or glowing) else 1
    rrect(surf, bord, r, r=8, bw=bw)

    if face_down:
        inner = pygame.Rect(rx+4, ry+4, w-8, h-8)
        rrect(surf, (20,26,40), inner, r=6)
        rrect(surf, BORDER, inner, r=6, bw=1)
        # Diamond pattern
        cx2, cy2 = rx+w//2, ry+h//2
        for radius in (12, 22, 32):
            pts = [(cx2+int(radius*math.cos(math.radians(a))),
                    cy2+int(radius*0.7*math.sin(math.radians(a))))
                   for a in range(0,360,90)]
            pygame.draw.polygon(surf, BORDER, pts, 1)
        return

    if cd is None: return

    accent = card_accent(cd)

    # Accent stripe
    pygame.draw.rect(surf, accent,
                     pygame.Rect(rx+1, ry+1, w-2, 5),
                     border_top_left_radius=7, border_top_right_radius=7)

    # Image
    img_h = h - 32
    img   = load_img(cd["image"], w-4, img_h)
    if greyed:
        gs = img.copy(); gs.fill((0,0,0,130), special_flags=pygame.BLEND_RGBA_MULT)
        surf.blit(gs, (rx+2, ry+7))
    else:
        surf.blit(img, (rx+2, ry+7))

    # Name bar at bottom
    name_bar = pygame.Rect(rx+1, ry+h-22, w-2, 21)
    pygame.draw.rect(surf, (12,16,26,200), name_bar,
                     border_bottom_left_radius=7, border_bottom_right_radius=7)

    name = cd["name"]
    ns   = fonts["small"].render(name, True, WHITE if not greyed else MUTED)
    if ns.get_width() > w-6:
        ns = fonts["tiny"].render(name, True, WHITE if not greyed else MUTED)
    surf.blit(ns, (rx+w//2-ns.get_width()//2, ry+h-19))

    # Value orb
    value = cd.get("value")
    if value is not None:
        draw_value_orb(surf, value, rx+13, ry+h-13, MUTED if greyed else accent, fonts["tiny"], 11)

    # Played indicator
    if played:
        pt = fonts["tiny"].render("▶ PLAYED", True, GREEN)
        surf.blit(pt, (rx+w//2-pt.get_width()//2, ry+7))

# ══════════════════════════════════════════════════════════════════════
# Sidebar card preview
# ══════════════════════════════════════════════════════════════════════
class CardPreview:
    def __init__(self, display, fonts):
        self.display = display
        self.fonts   = fonts
        self.card    = None
        self.label   = ""

    def set_card(self, cd, label=""):
        self.card, self.label = cd, label

    def clear_preview(self):
        self.card, self.label = None, ""

    def draw(self, sx, cy, pw):
        fs, fn, fl, fd = (self.fonts[k] for k in ("small","normal","large","desc"))

        if self.card is None:
            for txt, col in [("Hover a card", MUTED), ("to preview it", DIM)]:
                s = fs.render(txt, True, col)
                self.display.blit(s, (sx+pw//2-s.get_width()//2, cy))
                cy += s.get_height() + 4
            return cy + 8

        accent = card_accent(self.card)

        # Accent bar
        pygame.draw.rect(self.display, accent, pygame.Rect(sx, cy, pw, 5),
                         border_top_left_radius=6, border_top_right_radius=6)
        cy += 7

        # Image
        iw = pw - 4; ih = int(iw * 0.88)
        img = load_img(self.card["image"], iw, ih)
        self.display.blit(img, (sx+2, cy)); cy += ih+6

        # Name
        ns = fl.render(self.card["name"], True, WHITE)
        if ns.get_width() > pw: ns = fn.render(self.card["name"], True, WHITE)
        self.display.blit(ns, (sx+pw//2-ns.get_width()//2, cy)); cy += ns.get_height()+4

        # Category + label on same line
        cat  = self.card.get("category","").upper()
        cs   = fs.render(cat, True, accent)
        self.display.blit(cs, (sx+pw//2-cs.get_width()//2, cy))
        cy += cs.get_height()+4
        if self.label:
            lt = fs.render(self.label, True, TEAL)
            self.display.blit(lt, (sx+pw//2-lt.get_width()//2, cy))
            cy += lt.get_height()+4

        # Value orb
        value = self.card.get("value")
        if value is not None:
            orb_r  = 18; orb_cx = sx+pw//2; orb_cy = cy+orb_r
            pygame.draw.circle(self.display, accent, (orb_cx,orb_cy), orb_r)
            pygame.draw.circle(self.display, PANEL2,  (orb_cx,orb_cy), orb_r-3)
            pygame.draw.circle(self.display, accent, (orb_cx,orb_cy), orb_r-7)
            vs = fn.render(str(value), True, WHITE)
            self.display.blit(vs, (orb_cx-vs.get_width()//2, orb_cy-vs.get_height()//2))
            cy += orb_r*2+8

        pygame.draw.line(self.display, BORDER, (sx+4,cy), (sx+pw-4,cy), 1); cy += 6

        # Description
        desc = self.card.get("desc","")
        if desc:
            for line in wrap_text(fd, desc, pw-8):
                ds = fd.render(line, True, MUTED)
                self.display.blit(ds, (sx+4, cy)); cy += ds.get_height()+2
            cy += 4

        # Beats / countered-by
        beats = BEATS.get(self.card["name"], [])
        if beats:
            pygame.draw.line(self.display, BORDER, (sx+4,cy), (sx+pw-4,cy), 1); cy += 5
            bt = fs.render("Beats:", True, GREEN)
            self.display.blit(bt, (sx+4, cy)); cy += bt.get_height()+2
            for bname in beats:
                bs = self.fonts["tiny"].render(f"  • {bname}", True, MUTED)
                self.display.blit(bs, (sx+4, cy)); cy += bs.get_height()+1
            cy += 4

        pygame.draw.line(self.display, BORDER, (sx+4,cy), (sx+pw-4,cy), 1); cy += 8
        return cy

# ══════════════════════════════════════════════════════════════════════
# Zone pile  (deck / graveyard / banished)
# ══════════════════════════════════════════════════════════════════════
class ZonePile:
    def __init__(self, label, pos, img_path, color=MUTED):
        self.label = label
        self.pos   = pos
        self.color = color
        self.cards = []
        self._img  = load_img(img_path, ZONE_W-4, ZONE_H-24) if os.path.exists(img_path) else None
        self.rect  = pygame.Rect(pos[0], pos[1], ZONE_W, ZONE_H)

    def draw(self, surf, fonts):
        x, y = self.pos
        rrect(surf, PANEL, self.rect, r=7)
        rrect(surf, self.color, self.rect, r=7, bw=1)
        if self._img:
            surf.blit(self._img, (x+2, y+2))
        else:
            t = fonts["normal"].render(self.label[0], True, self.color)
            surf.blit(t, (x+ZONE_W//2-t.get_width()//2, y+ZONE_H//2-t.get_height()//2))
        cs = fonts["tiny"].render(f"{self.label} {len(self.cards)}", True, self.color)
        surf.blit(cs, (x+ZONE_W//2-cs.get_width()//2, y+ZONE_H-16))

    def hovered(self): return self.rect.collidepoint(pygame.mouse.get_pos())

# ══════════════════════════════════════════════════════════════════════
# HP bar widget
# ══════════════════════════════════════════════════════════════════════
class HPBar:
    def __init__(self, display, fonts, x, y, w=220):
        self.display = display
        self.fonts   = fonts
        self.x, self.y, self.w = x, y, w
        self._display_hp = float(MAX_HP)   # smoothed value

    def update(self, target_hp):
        self._display_hp += (target_hp - self._display_hp) * 0.12

    def draw(self, label, hp, is_player=True):
        x, y, w = self.x, self.y, self.w
        col = GREEN if hp > MAX_HP * 0.5 else AMBER if hp > MAX_HP * 0.25 else RED

        self.fonts["small"]  # just access to avoid unused
        ls = self.fonts["normal"].render(f"{label}: {hp}/{MAX_HP}", True, WHITE)
        self.display.blit(ls, (x, y))

        bg = pygame.Rect(x, y+22, w, 10)
        rrect(self.display, PANEL2, bg, r=5)
        fw = int(w * clamp(hp, 0, MAX_HP) / MAX_HP)
        if fw > 0:
            rrect(self.display, col, pygame.Rect(x, y+22, fw, 10), r=5)
        rrect(self.display, BORDER, bg, r=5, bw=1)

# ══════════════════════════════════════════════════════════════════════
# Main Game class
# ══════════════════════════════════════════════════════════════════════
class Game:
    HAND_SIZE    = 5
    DOUBLE_CLICK = 380

    def __init__(self, display):
        self.display = display

        self.fonts = {
            "normal": pygame.font.Font(None, 26),
            "small":  pygame.font.Font(None, 21),
            "large":  pygame.font.Font(None, 44),
            "title":  pygame.font.Font(None, 34),
            "desc":   pygame.font.Font(None, 20),
            "tiny":   pygame.font.Font(None, 17),
            "huge":   pygame.font.Font(None, 72),
        }

        self._init_state()

        self.preview    = CardPreview(display, self.fonts)
        self.p_hp_bar   = HPBar(display, self.fonts, PAD, HEIGHT-62)
        self.e_hp_bar   = HPBar(display, self.fonts, PAD, 60)

        self.p_deck_zone  = ZonePile("Deck",   DECK_POS,  "assets/deck_image.png",      BLUE)
        self.p_grave_zone = ZonePile("Grave",  GRAVE_POS, "assets/graveyard_image.png", MUTED)
        self.p_ban_zone   = ZonePile("Banish", BAN_POS,   "assets/banished_icon.png",   AMBER)
        self.e_deck_zone  = ZonePile("Deck",   E_DECK_POS,  "assets/deck_image.png",    RED)
        self.e_grave_zone = ZonePile("Grave",  E_GRAVE_POS, "assets/graveyard_image.png",MUTED)
        self.e_ban_zone   = ZonePile("Banish", E_BAN_POS,   "assets/banished_icon.png", AMBER)

        self.floats: list[FloatText] = []

        self._log("Game started")
        self._log(f"Player draws {self.HAND_SIZE} cards")

    # ─── state init / reset ──────────────────────────────────────────
    def _init_state(self):
        deck = [c for c in STARTING_DECK if c in CARD_BY_NAME]
        random.shuffle(deck)
        self.player_deck      = deck[:]
        self.player_hand      = []
        self.player_field     = []      # list of names, max FIELD_SLOTS
        self.player_graveyard = []
        self.player_banished  = []
        self.player_hp        = MAX_HP

        edeck = deck[:]
        random.shuffle(edeck)
        self.enemy_deck      = edeck
        self.enemy_hand      = []
        self.enemy_field     = []
        self.enemy_graveyard = []
        self.enemy_banished  = []
        self.enemy_hp        = MAX_HP

        self.selected_hand_idx = -1
        self.dragging          = False
        self.drag_card_name    = None
        self.drag_pos          = (0,0)

        self.status       = ""
        self.status_timer = 0
        self.round        = 1
        self.phase        = "draw"
        self.result       = None
        self.result_timer = 0    # auto-clear result banner after N frames
        self.game_over    = False
        self.winner       = None

        self.show_graveyard = False
        self.show_banished  = False
        self.show_history   = False
        self.show_hand      = True
        self.show_end_turn = False
        self.history_log    = []
        self.last_click_time = 0

        self._draw_cards(self.HAND_SIZE)
        self._enemy_draw(self.HAND_SIZE)

    # ─── helpers ──────────────────────────────────────────────────────
    def _txt(self, text, x, y, color=WHITE, fk="normal"):
        s = self.fonts[fk].render(text, True, color)
        self.display.blit(s, (x, y))

    def set_status(self, msg):
        self.status, self.status_timer = msg, STATUS_DUR

    def tick_status(self):
        if self.status_timer > 0:
            self.status_timer -= 1
            if self.status_timer == 0: self.status = ""

    def _log(self, msg):
        self.history_log.append(f"R{self.round}: {msg}")
        if len(self.history_log) > 40: self.history_log.pop(0)

    def _float(self, text, x, y, color=WHITE, size=30):
        self.floats.append(FloatText(text, x, y, color, size))

    def _draw_cards(self, n=1):
        for _ in range(n):
            if self.player_deck:
                self.player_hand.append(self.player_deck.pop())

    def _enemy_draw(self, n=1):
        for _ in range(n):
            if self.enemy_deck:
                self.enemy_hand.append(self.enemy_deck.pop())

    # ─── layout helpers ───────────────────────────────────────────────
    def _hand_rect(self, idx):
        n       = len(self.player_hand)
        spacing = min(CARD_W + 12, (SIDEBAR_X - 120) // max(1, n))
        sx      = (SIDEBAR_X - n * spacing) // 2
        lift    = 16 if idx == self.selected_hand_idx else 0
        return pygame.Rect(sx + idx * spacing, HAND_Y - lift, CARD_W, CARD_H)

    def _field_rect(self, idx):
        mid_y = FIELD_Y + FIELD_H // 2
        sx    = FIELD_X + (FIELD_W - FIELD_SLOTS * FIELD_SLOT_W) // 2
        return pygame.Rect(sx + idx * FIELD_SLOT_W + 4, mid_y + 10, CARD_W, CARD_H)

    def _enemy_field_rect(self, idx):
        sx = FIELD_X + (FIELD_W - FIELD_SLOTS * FIELD_SLOT_W) // 2
        return pygame.Rect(sx + idx * FIELD_SLOT_W + 4, FIELD_Y + 10, CARD_W, CARD_H)

    def _in_field_zone(self, pos):
        return pygame.Rect(FIELD_X, FIELD_Y + FIELD_H//2, FIELD_W, FIELD_H//2).collidepoint(pos)

    # ─── game actions ─────────────────────────────────────────────────
    def _play_to_field(self, hand_idx):
        if len(self.player_field) >= FIELD_SLOTS:
            self.set_status("Field full!")
            return
        name = self.player_hand.pop(hand_idx)
        self.player_field.append(name)
        self.selected_hand_idx = -1
        self._log(f"Player plays {name}")
        self.set_status(f"Played {name}")
        r = self._field_rect(len(self.player_field)-1)
        self._float(f"+{name}", r.centerx, r.y, TEAL)
        self.preview.set_card(CARD_BY_NAME.get(name), "on field")

    def _resolve_battle(self):
        p_names = self.player_field[:]
        e_names = self.enemy_field[:] if self.enemy_field else [
            random.choice(["Rock","Paper","Scissors"])]

        p_wins = sum(1 for pn in p_names for en in e_names if en in BEATS.get(pn,[]))
        e_wins = sum(1 for en in e_names for pn in p_names if pn in BEATS.get(en,[]))

        if p_wins > e_wins:
            self.result  = "Player Wins"
            dmg = p_wins - e_wins
            self.enemy_hp = max(0, self.enemy_hp - dmg)
            self._log(f"Player wins round! -{dmg} enemy HP")
            self._float(f"-{dmg} HP", FIELD_X + FIELD_W//2, FIELD_Y + 30, RED, 36)
        elif e_wins > p_wins:
            self.result  = "Enemy Wins"
            dmg = e_wins - p_wins
            self.player_hp = max(0, self.player_hp - dmg)
            self._log(f"Enemy wins round! -{dmg} player HP")
            self._float(f"-{dmg} HP", FIELD_X + FIELD_W//2, FIELD_Y + FIELD_H - 50, RED, 36)
        elif not p_names:
            self.result  = "Enemy Wins"
            self.player_hp = max(0, self.player_hp - 1)
            self._log("Enemy wins (no cards played)")
            self._float("-1 HP", FIELD_X + FIELD_W//2, HAND_Y, RED, 36)
        else:
            self.result = "Draw"
            self._log("Round draws")

        self.result_timer = 180

        # Field → graveyard
        self.player_graveyard.extend(self.player_field)
        self.enemy_graveyard.extend(self.enemy_field)
        self.player_field.clear()
        self.enemy_field.clear()
        self.set_status(f"Round {self.round}: {self.result}")

        # Check game over
        if self.player_hp <= 0:
            self.game_over = True; self.winner = "Enemy"
            self._log("GAME OVER — Enemy wins the match!")
        elif self.enemy_hp <= 0:
            self.game_over = True; self.winner = "Player"
            self._log("GAME OVER — Player wins the match!")

    def _end_turn(self):
        self.show_end_turn = True
        if self.game_over: return

        # Enemy AI: play best card against player field
        if self.enemy_hand:
            best = None
            for ec in self.enemy_hand:
                for pc in self.player_field:
                    if pc in BEATS.get(ec, []):
                        best = ec; break
                if best: break
            played = best or random.choice(self.enemy_hand)
            self.enemy_hand.remove(played)
            self.enemy_field.append(played)
            self._log(f"Enemy plays a card")

        self._resolve_battle()
        self.round  += 1
        self.phase   = "draw"

        drawn_p = min(2, max(0, self.HAND_SIZE - len(self.player_hand)))
        drawn_e = min(2, max(0, self.HAND_SIZE - len(self.enemy_hand)))
        self._draw_cards(drawn_p)
        self._enemy_draw(drawn_e)
        if drawn_p: self._log(f"Player draws {drawn_p}")
        if drawn_e: self._log(f"Enemy draws {drawn_e}")

    # ══════════════════════════════════════════════════════════════════
    # Events
    # ══════════════════════════════════════════════════════════════════
    def handle_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT: return False

            elif e.type == pygame.MOUSEMOTION:
                self.drag_pos = e.pos
                if not self.dragging:
                    self._hover_update(e.pos)

            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                self._on_click(e.pos)

            elif e.type == pygame.MOUSEBUTTONUP and e.button == 1:
                self._on_release(e.pos)

            elif e.type == pygame.KEYDOWN:
                key = e.key
                if   key == pygame.K_ESCAPE: return self._nav_back()
                elif key == pygame.K_e and not self.game_over and not self.show_end_turn: self._end_turn()
                elif key == pygame.K_e and self.show_end_turn: self.show_end_turn = False
                elif key == pygame.K_SPACE:
                    self.show_hand = not self.show_hand
                elif key == pygame.K_c:
                    self.preview.clear_preview()
                elif key == pygame.K_d and not self.game_over:
                    self._draw_cards(1); self.set_status("Drew a card")
                elif key == pygame.K_r and not self.game_over:
                    self.player_field.clear()
                    self.selected_hand_idx = -1
                    self.set_status("Field cleared")
                elif key == pygame.K_n and self.game_over:
                    self._init_state()
                    self.set_status("New game started!")
                elif key == pygame.K_h:
                    self.show_history   = not self.show_history
                    self.show_graveyard = self.show_banished = False
                elif key == pygame.K_g:
                    self.show_graveyard = not self.show_graveyard
                    self.show_history   = self.show_banished = False
                elif key == pygame.K_b:
                    self.show_banished  = not self.show_banished
                    self.show_history   = self.show_graveyard = False
                # Number keys select hand card
                for ki in range(1, 10):
                    if key == getattr(pygame, f"K_{ki}", None):
                        idx = ki - 1
                        if idx < len(self.player_hand):
                            self.selected_hand_idx = idx
                            name = self.player_hand[idx]
                            self.preview.set_card(CARD_BY_NAME.get(name), "in hand")

        return True

    def _nav_back(self):
        if _cardgame: _cardgame.main()
        return False

    def _hover_update(self, pos):
        for i in range(len(self.player_hand)):
            if self._hand_rect(i).collidepoint(pos):
                name = self.player_hand[i]
                self.preview.set_card(CARD_BY_NAME.get(name), "in hand"); return
        for i in range(len(self.player_field)):
            if self._field_rect(i).collidepoint(pos):
                name = self.player_field[i]
                self.preview.set_card(CARD_BY_NAME.get(name), "on field"); return
        for i in range(len(self.enemy_field)):
            if self._enemy_field_rect(i).collidepoint(pos):
                name = self.enemy_field[i]
                self.preview.set_card(CARD_BY_NAME.get(name), "enemy field"); return

    def _on_click(self, pos):
        now    = pygame.time.get_ticks()
        double = (now - self.last_click_time) <= self.DOUBLE_CLICK
        self.last_click_time = now

        if self.game_over: return

        # Buttons
        if self._btn_end_rect().collidepoint(pos): self._end_turn(); return
        if self._btn_draw_rect().collidepoint(pos): self._draw_cards(1); self.set_status("Drew a card"); return

        # Double-click hand → play
        if double:
            for i in range(len(self.player_hand)):
                if self._hand_rect(i).collidepoint(pos):
                    self._play_to_field(i); return

        # Single-click hand → select + start drag
        for i in range(len(self.player_hand)):
            if self._hand_rect(i).collidepoint(pos):
                self.selected_hand_idx = i
                self.dragging          = True
                self.drag_card_name    = self.player_hand[i]
                name = self.player_hand[i]
                self.preview.set_card(CARD_BY_NAME.get(name), "in hand")
                return

        # Click field card
        for i in range(len(self.player_field)):
            if self._field_rect(i).collidepoint(pos):
                name = self.player_field[i]
                self.preview.set_card(CARD_BY_NAME.get(name), "on field"); return

    def _on_release(self, pos):
        if self.dragging and self.drag_card_name:
            if self._in_field_zone(pos) and self.drag_card_name in self.player_hand:
                idx = self.player_hand.index(self.drag_card_name)
                self._play_to_field(idx)
        self.dragging       = False
        self.drag_card_name = None

    # ── button rects ──────────────────────────────────────────────────
    def _btn_end_rect(self):
        return pygame.Rect(SIDEBAR_X - 196, HEIGHT - 62, 168, 46)

    def _btn_draw_rect(self):
        return pygame.Rect(SIDEBAR_X - 386, HEIGHT - 62, 168, 46)

    # ══════════════════════════════════════════════════════════════════
    # Drawing
    # ══════════════════════════════════════════════════════════════════
    def _draw_header(self):
        bar = pygame.Rect(0, 0, SIDEBAR_X, 52)
        rrect(self.display, PANEL, bar, r=0)
        pygame.draw.line(self.display, BORDER, (0,52), (SIDEBAR_X,52), 1)
        self._txt("✦  Card Duel", 16, 12, WHITE, "title")
        phase_col = {"draw":TEAL,"main":BLUE,"battle":RED,"end":AMBER}.get(self.phase, MUTED)
        self._txt(f"Phase: {self.phase.upper()}", 230, 14, phase_col, "small")
        self._txt(f"Round {self.round}", 380, 14, MUTED, "small")
        # right-aligned: deck size
        dk = self.fonts["small"].render(f"Deck: {len(self.player_deck)}", True, DIM)
        self.display.blit(dk, (SIDEBAR_X - dk.get_width() - 50, 16))

    def _draw_field(self):
        fr   = pygame.Rect(FIELD_X, FIELD_Y, FIELD_W, FIELD_H)
        mid  = FIELD_Y + FIELD_H // 2
        hov  = fr.collidepoint(pygame.mouse.get_pos()) and self.dragging
        rrect(self.display, FIELD_ACTIVE if hov else FIELD_IDLE, fr, r=12)
        rrect(self.display, TEAL if hov else BORDER, fr, r=12, bw=2 if hov else 1)

        # Enemy zone tint
        ez = pygame.Rect(FIELD_X+1, FIELD_Y+1, FIELD_W-2, FIELD_H//2-1)
        pygame.draw.rect(self.display, ENEMY_BG, ez, border_top_left_radius=11, border_top_right_radius=11)

        # Divider
        pygame.draw.line(self.display, FIELD_SEP, (FIELD_X+10, mid), (FIELD_X+FIELD_W-10, mid), 2)

        # Labels
        self._txt("ENEMY", FIELD_X+8, FIELD_Y+8, DIM, "tiny")
        self._txt("PLAYER FIELD", FIELD_X+8, mid+8, DIM, "tiny")

        # Empty slot ghosts
        for i in range(FIELD_SLOTS):
            pr = self._field_rect(i)
            if i >= len(self.player_field):
                rrect(self.display, PANEL2, pr, r=8)
                rrect(self.display, BORDER, pr, r=8, bw=1)
                t = self.fonts["tiny"].render("drop here", True, DIM)
                self.display.blit(t, (pr.centerx-t.get_width()//2, pr.centery-6))
            er = self._enemy_field_rect(i)
            if i >= len(self.enemy_field):
                rrect(self.display, (18,14,22), er, r=8)
                rrect(self.display, BORDER, er, r=8, bw=1)

        # Player cards
        for i, name in enumerate(self.player_field):
            r = self._field_rect(i)
            draw_card_tile(self.display, self.fonts, CARD_BY_NAME.get(name),
                           r.x, r.y, CARD_W, CARD_H)

        # Enemy cards
        revealed = (self.result is not None)
        for i, name in enumerate(self.enemy_field):
            r = self._enemy_field_rect(i)
            draw_card_tile(self.display, self.fonts, CARD_BY_NAME.get(name),
                           r.x, r.y, CARD_W, CARD_H, face_down=not revealed)

    def _draw_hand(self):
        hp = pygame.Rect(0, HAND_Y - 18, SIDEBAR_X, CARD_H + 28)
        panel(self.display, hp, r=0)

        n = len(self.player_hand)
        hand_label = f"Hand  {n}"
        self._txt(hand_label, PAD, HAND_Y - 14, MUTED, "small")
        # Hint
        hint = self.fonts["tiny"].render("1-9 to select  ·  dbl-click or drag to field", True, DIM)
        self.display.blit(hint, (SIDEBAR_X - hint.get_width() - 10, HAND_Y - 14))

        for i in range(n):
            r   = self._hand_rect(i)
            sel = (i == self.selected_hand_idx)
            draw_card_tile(self.display, self.fonts, CARD_BY_NAME.get(self.player_hand[i]),
                           r.x, r.y, CARD_W, CARD_H, selected=sel)
            # Index badge
            idx_s = self.fonts["tiny"].render(str(i+1), True, TEAL if sel else DIM)
            self.display.blit(idx_s, (r.x + CARD_W//2 - idx_s.get_width()//2, r.y + CARD_H + 2))

    def _draw_player_hand(self):
        n       = len(self.player_hand)
        spacing = min(E_CARD_W + 8, 500 // max(1, n))
        sx      = FIELD_X + 200 + 20
        for i in range(n):
            draw_card_tile(self.display, self.fonts, None, sx + i * spacing, HAND_Y, E_CARD_W, E_CARD_H, face_down=True)
        self._txt(f"Player hand: {n}", sx, HAND_Y + E_CARD_H + 4, DIM, "tiny")

    def _draw_enemy_hand(self):
        n       = len(self.enemy_hand)
        spacing = min(E_CARD_W + 8, 500 // max(1, n))
        sx      = FIELD_X + 200 + 20 # FIELD_X + FIELD_W + 20
        for i in range(n):
            draw_card_tile(self.display, self.fonts, None, sx + i * spacing, E_HAND_Y, E_CARD_W, E_CARD_H, face_down=True)
        self._txt(f"Enemy hand: {n}", sx, E_HAND_Y + E_CARD_H + 4, DIM, "tiny")

    def _draw_hp_bars(self):
        self.p_hp_bar.update(self.player_hp)
        self.e_hp_bar.update(self.enemy_hp)
        self.p_hp_bar.draw("Player HP", self.player_hp, True)
        self.e_hp_bar.draw("Enemy HP",  self.enemy_hp,  False)

    def _draw_zones(self):
        for zone, cards in [
            (self.p_deck_zone,  self.player_deck),
            (self.p_grave_zone, self.player_graveyard),
            (self.p_ban_zone,   self.player_banished),
            (self.e_deck_zone,  self.enemy_deck),
            (self.e_grave_zone, self.enemy_graveyard),
            (self.e_ban_zone,   self.enemy_banished),
        ]:
            zone.cards = cards
            zone.draw(self.display, self.fonts)

    def _draw_buttons(self):
        for rect, label, color, key in [
            (self._btn_draw_rect(), "D  Draw",    TEAL, None),
            (self._btn_end_rect(),  "E  End Turn", RED,  None),
        ]:
            hov = rect.collidepoint(pygame.mouse.get_pos())
            bg  = lerp_color(PANEL2, color, 0.18 if hov else 0)
            rrect(self.display, bg, rect, r=9)
            rrect(self.display, color if hov else BORDER, rect, r=9, bw=1)
            t = self.fonts["normal"].render(label, True, WHITE if hov else color)
            self.display.blit(t, (rect.centerx - t.get_width()//2, rect.centery - t.get_height()//2))

    def _draw_result_banner(self):
        if not self.result or self.result_timer <= 0: return
        self.result_timer -= 1
        alpha = min(255, self.result_timer * 3)
        col   = GREEN if self.result == "Player Wins" else RED if self.result == "Enemy Wins" else AMBER
        t = self.fonts["large"].render(self.result, True, col)
        bx = WIDTH//2 - t.get_width()//2 - 24
        br = pygame.Rect(bx, FIELD_Y + FIELD_H//2 - 28, t.get_width()+48, 56)
        s  = pygame.Surface((br.w, br.h), pygame.SRCALPHA)
        pygame.draw.rect(s, (*PANEL2, alpha), (0,0,br.w,br.h), border_radius=10)
        pygame.draw.rect(s, (*col, alpha),    (0,0,br.w,br.h), 2, border_radius=10)
        self.display.blit(s, br.topleft)
        t.set_alpha(alpha)
        self.display.blit(t, (bx+24, br.centery - t.get_height()//2))

    def _draw_game_over(self):
        if not self.game_over: return
        dim = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        dim.fill((0,0,0,170))
        self.display.blit(dim, (0,0))
        col  = GREEN if self.winner == "Player" else RED
        msg  = "YOU WIN!" if self.winner == "Player" else "YOU LOSE"
        t    = self.fonts["huge"].render(msg, True, col)
        self.display.blit(t, (WIDTH//2-t.get_width()//2, HEIGHT//2-60))
        sub  = self.fonts["normal"].render("Press N for new game  ·  ESC to exit", True, MUTED)
        self.display.blit(sub, (WIDTH//2-sub.get_width()//2, HEIGHT//2+40))

    def _draw_overlay(self, title, lines):
        ox, oy, ow, oh = WIDTH//4, HEIGHT//5, WIDTH//2, HEIGHT*3//5
        rrect(self.display, PANEL2, pygame.Rect(ox,oy,ow,oh), r=12)
        rrect(self.display, BORDER, pygame.Rect(ox,oy,ow,oh), r=12, bw=1)
        tl = self.fonts["title"].render(title, True, WHITE)
        self.display.blit(tl, (ox+ow//2-tl.get_width()//2, oy+14))
        pygame.draw.line(self.display, BORDER, (ox+10,oy+44), (ox+ow-10,oy+44), 1)
        visible = lines[-24:]
        for i, line in enumerate(visible):
            lt = self.fonts["small"].render(line, True, MUTED)
            self.display.blit(lt, (ox+20, oy+52+i*22))
        # Close hint
        ch = self.fonts["tiny"].render("Press key again to close", True, DIM)
        self.display.blit(ch, (ox+ow-ch.get_width()-12, oy+oh-20))

    def _draw_floats(self):
        for ft in self.floats:
            ft.update(); ft.draw(self.display)
        self.floats = [f for f in self.floats if f.alive]

    def _draw_drag_ghost(self):
        if not self.dragging or not self.drag_card_name: return
        cd = CARD_BY_NAME.get(self.drag_card_name)
        dx = self.drag_pos[0] - CARD_W//2
        dy = self.drag_pos[1] - CARD_H//2
        ghost = pygame.Surface((CARD_W, CARD_H), pygame.SRCALPHA)
        pygame.draw.rect(ghost, (*BLUE,140), (0,0,CARD_W,CARD_H), border_radius=8)
        pygame.draw.rect(ghost, (*WHITE,200),(0,0,CARD_W,CARD_H), 1, border_radius=8)
        self.display.blit(ghost, (dx,dy))
        if cd:
            img = load_img(cd["image"], CARD_W-8, CARD_H-28)
            self.display.blit(img, (dx+4, dy+5))
        ns = self.fonts["small"].render(self.drag_card_name, True, WHITE)
        self.display.blit(ns, (dx+CARD_W//2-ns.get_width()//2, dy+CARD_H-18))

    def _draw_sidebar(self):
        sx = SIDEBAR_X; sw = WIDTH - sx
        panel(self.display, pygame.Rect(sx-8,0,sw+8,HEIGHT), r=0)

        self._txt("Card Duel",  sx+6, 16, WHITE, "title")
        phase_col = {"draw":TEAL,"main":BLUE,"battle":RED,"end":AMBER}.get(self.phase,MUTED)
        self._txt(self.phase.upper(), sx+6, 52, phase_col, "small")
        pygame.draw.line(self.display, BORDER, (sx,76), (WIDTH-4,76), 1)

        cy   = 84
        pw   = sw - 20

        cy = self.preview.draw(sx+6, cy, pw)



        show_hand_text = "Show Hand"
        hide_hand_text = "Hide Hand"
        show_hide_hand_text = ""
        if self.show_hand:
            show_hide_hand_text = hide_hand_text
        else:
            show_hide_hand_text = show_hand_text

        # Controls
        controls = [
            ("ESC","Main menu"), 
            ("SPACE", show_hide_hand_text), 
            ("C", "Clear Preview"), 
            ("E","End turn"),   
            ("D","Draw card"),
            ("R","Reset field"), 
            ("H","History"),    
            ("G","Graveyard"),
            ("B","Banished"),    
            ("N","New game"),
        ]
        for key, desc in controls:
            if cy + 26 > HEIGHT - 10: break
            kr = pygame.Rect(sx+6, cy, 26, 20)
            rrect(self.display, (32,44,62), kr, r=4)
            ks = self.fonts["small"].render(key, True, BLUE)
            self.display.blit(ks, (kr.centerx-ks.get_width()//2, kr.y+2))
            self._txt(desc, sx+38, cy+2, MUTED, "small")
            cy += 26

        pygame.draw.line(self.display, BORDER, (sx,cy+2),(WIDTH-4,cy+2),1); cy+=8

        hints = [("Dbl-click","play to field"), ("Drag","play to field"), ("1-9","select hand")]
        for lbl, act in hints:
            if cy+20 > HEIGHT-10: break
            self._txt(f"{lbl} → {act}", sx+6, cy, DIM, "small"); cy+=20

        pygame.draw.line(self.display, BORDER, (sx,cy+2),(WIDTH-4,cy+2),1); cy+=8

        stats = [
            ("Player HP", f"{self.player_hp}/{MAX_HP}", GREEN if self.player_hp > MAX_HP//2 else RED),
            ("Enemy HP",  f"{self.enemy_hp}/{MAX_HP}",  RED if self.enemy_hp <= MAX_HP//2 else MUTED),
            ("Deck",      str(len(self.player_deck)),   MUTED),
            ("Hand",      str(len(self.player_hand)),   MUTED),
            ("Graveyard", str(len(self.player_graveyard)), MUTED),
            ("Round",     str(self.round),              MUTED),
        ]
        for lbl, val, col in stats:
            if cy+20 > HEIGHT-10: break
            self._txt(f"{lbl}", sx+6, cy, MUTED, "small")
            vs = self.fonts["small"].render(val, True, col)
            self.display.blit(vs, (sx+pw-vs.get_width(), cy))
            cy += 20

        if self.status and cy+10 < HEIGHT:
            pygame.draw.line(self.display, BORDER, (sx,cy+2),(WIDTH-4,cy+2),1); cy+=8
            col = (GREEN if any(w in self.status for w in ("Wins","Drew","Played","started"))
                   else RED if any(w in self.status for w in ("full","Empty","Enemy","Lose"))
                   else WHITE)
            for line in wrap_text(self.fonts["small"], self.status, pw-4):
                if cy+20 > HEIGHT-10: break
                self._txt(line, sx+6, cy, col, "small"); cy += 20

    # ── main draw ─────────────────────────────────────────────────────
    def draw(self):
        self.tick_status()
        self.display.fill(BG)
        self._draw_header()
        
        self._draw_field()
        self._draw_enemy_hand()
        self._draw_zones()
        if self.show_hand == True:
            self._draw_hand()
        else:
            self._draw_player_hand()
        self._draw_buttons()
        
        
        self._draw_sidebar()
        self._draw_drag_ghost()




        if self.show_end_turn:
            items = [f"{i+1}. {n}" for i,n in enumerate(self.player_field)] or ["(empty)"] + [f"{i+1}. {n}" for i,n in enumerate(self.enemy_field)] or ["(empty)"]
            self._draw_overlay("End Turn", items)

        elif self.show_history:
            self._draw_overlay("History Log", self.history_log)
        elif self.show_graveyard:
            items = [f"{i+1}. {n}" for i,n in enumerate(self.player_graveyard)] or ["(empty)"]
            self._draw_overlay("Player Graveyard", items)
        elif self.show_banished:
            items = [f"{i+1}. {n}" for i,n in enumerate(self.player_banished)] or ["(empty)"]
            self._draw_overlay("Player Banished", items)
        
        self._draw_hp_bars()
        self._draw_result_banner()
        self._draw_floats()

        

        if self.game_over:
            self._draw_game_over()


# ══════════════════════════════════════════════════════════════════════
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