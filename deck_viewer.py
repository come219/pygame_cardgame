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
# Palette  (dark slate / teal accent)
# =====================
BG             = (12,  14,  20 )
PANEL          = (20,  24,  34 )
PANEL2         = (26,  30,  42 )
BORDER         = (38,  46,  64 )
BORDER_HI      = (60,  80, 120 )
CARD_BG        = (30,  36,  50 )
CARD_HOV       = (44,  54,  76 )
CARD_GREY      = (18,  20,  26 )
CARD_BORD      = (50,  62,  88 )
CARD_BORD_ACT  = (80, 160, 220 )
WHITE          = (225, 232, 245)
MUTED          = (95,  108, 132)
DIM            = (55,  65,  85 )
RED            = (210,  65,  65)
AMBER          = (215, 155,  45)
BLUE           = (75,  145, 255)
TEAL           = (45,  195, 165)
GREEN          = (65,  190,  95)
PURPLE         = (145,  90, 220)
OVERLAY        = (8,   10,  16, 225)

CARD_W, CARD_H   = 108, 148
MAX_DECK         = 30
STATUS_DUR       = 150

# Deck selector
DS_W, DS_H = 260, 360
DS_GAP     = 44

# =====================
# Layout regions (x, y, w, h)
# =====================
PAD          = 14
SIDEBAR_X    = 1490          # right panel start
TABS_Y       = 8
TABS_H       = 44

DECK_LABEL_Y = TABS_Y + TABS_H + 10
DECK_Y       = DECK_LABEL_Y + 22

COLL_LABEL_Y = 590
COLL_Y       = COLL_LABEL_Y + 22

# No more left preview panel — grid starts at left edge
DECK_PANEL_W = SIDEBAR_X - PAD * 2
COLL_PANEL_W = DECK_PANEL_W

# columns available for cards
CARD_COLS    = 11
CARD_CW      = CARD_W + 10
CARD_CH      = CARD_H + 10

# visible rows before scroll kicks in
DECK_VIS_ROWS = 2          # 2 rows = cards visible
COLL_VIS_ROWS = 2

DECK_VIS_H   = DECK_VIS_ROWS * CARD_CH
COLL_VIS_H   = COLL_VIS_ROWS * CARD_CH

DECK_PANEL_X = PAD
COLL_PANEL_X = DECK_PANEL_X

DECK_DEFS = [
    {"key": "a", "label": "Deck A", "image": "assets/deck_a_image.png"},
    {"key": "b", "label": "Deck B", "image": "assets/deck_b_image.png"},
    {"key": "c", "label": "Deck C", "image": "assets/deck_c_image.png"},
]

# =====================
# Expanded card pool with descriptions
# =====================
CARD_DESCRIPTIONS = {
    # Elements
    "Rock":          "The classic. Solid and dependable. Crushes through with brute force.",
    "Paper":         "Covers Rock and disproves Spock. Deceptively powerful.",
    "Scissors":      "Sharp and precise. Cuts through Paper with ease.",
    "Fire":          "Primal flame that consumes all. Burns through defenses.",
    "Water":         "The great equalizer. Extinguishes fire and erodes stone.",
    "Wind":          "Invisible force of nature. Carries storms and fuels flames.",
    "Earth":         "Solid and unyielding. The foundation upon which all is built.",
    "Lightning":     "Raw electrical energy. Strikes fast and devastates.",
    "Ice":           "Frozen power that slows and shatters. Chilling precision.",
    "Shadow":        "Darkness incarnate. Strikes from where you least expect.",
    "Light":         "Radiant energy that pierces darkness. Purifies and reveals.",
    "Void":          "The absence of everything. Consumes matter and energy alike.",
    # Units
    "Knight":        "Mounted warrior with lance and honor. Charges through enemy lines.",
    "Archer":        "Ranged combatant with deadly aim. Picks off threats from afar.",
    "Mage":          "Channels arcane magic. Versatile and unpredictable in combat.",
    "Dragon":        "A mighty beast of fire and fury. Dominates the skies.",
    "Goblin":        "Small but cunning. Overwhelms foes with numbers and tricks.",
    "Shield":        "Pure defense. Absorbs damage and protects allies.",
    "Rogue":         "Strikes from the shadows. Quick, silent, and deadly.",
    "Paladin":       "Holy warrior combining faith and steel. Heals and fights.",
    "Necromancer":   "Raises the dead to fight. Dark magic at its finest.",
    "Berserker":     "Uncontrollable rage fuels devastating attacks. All offense.",
    "Ranger":        "Master of the wilderness. Tracks and ambushes with precision.",
    "Druid":         "Nature's champion. Shapeshifts and commands the wild.",
    # Suited
    "Ace of Spades":      "The highest card. A symbol of power and finality.",
    "King of Hearts":     "The benevolent ruler. Strong leadership on the field.",
    "Queen of Diamonds":  "Elegant and sharp. Wealth becomes a weapon.",
    "Jack of Clubs":      "The resourceful knave. Tricks and cunning in play.",
    "Ten of Spades":      "A solid foundation. Reliable and consistent.",
    "Nine of Hearts":     "The wish card. Brings hope and unexpected turns.",
    "Eight of Diamonds":  "Steady and balanced. A dependable mid-range card.",
    "Seven of Clubs":     "Lucky number seven. Fortune favors the bold.",
    # Spells
    "Fireball":      "A blazing sphere of destruction. Deals massive area damage.",
    "Blizzard":      "A freezing storm that slows and damages all enemies.",
    "Thunderstrike": "A bolt from above. Precise and devastating single-target.",
    "Heal":          "Restores health to an ally. Essential for survival.",
    "Barrier":       "Creates a protective shield. Blocks incoming damage.",
    "Summon":        "Calls forth a creature to aid in battle.",
    "Curse":         "Weakens an enemy with dark magic. Reduces their power.",
    "Bless":         "Empowers an ally with divine energy. Boosts their strength.",
    "Teleport":      "Instantly moves a unit to a new position. Tactical repositioning.",
    "Drain":         "Siphons life force from an enemy. Heals you as it hurts them.",
}

ALL_CARDS = [
    # Elements
    "Rock", "Paper", "Scissors", "Fire", "Water", "Wind", "Earth", "Lightning",
    "Ice", "Shadow", "Light", "Void",
    # Units
    "Knight", "Archer", "Mage", "Dragon", "Goblin", "Shield",
    "Rogue", "Paladin", "Necromancer", "Berserker", "Ranger", "Druid",
    # Suited (standard)
    "Ace of Spades", "King of Hearts", "Queen of Diamonds", "Jack of Clubs",
    "Ten of Spades",  "Nine of Hearts", "Eight of Diamonds", "Seven of Clubs",
    # Spells
    "Fireball", "Blizzard", "Thunderstrike", "Heal", "Barrier", "Summon",
    "Curse", "Bless", "Teleport", "Drain",
]


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


def wrap_text(font, text, max_width):
    """Wrap text to fit within max_width. Returns list of lines."""
    words = text.split(' ')
    lines = []
    current = ""
    for word in words:
        test = (current + " " + word).strip()
        if font.size(test)[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


# =====================
# Scrollable card grid
# =====================
class CardGrid:
    """
    Renders a scrollable grid of cards inside a clipping rect.
    Cards are laid out left-to-right, top-to-bottom.
    Scroll with mouse wheel when hovering the grid area.
    """

    def __init__(self, display, clip_rect, cols=CARD_COLS):
        self.display   = display
        self.clip_rect = clip_rect   # pygame.Rect — visible area
        self.cols      = cols
        self.scroll_y  = 0           # pixels scrolled down
        self._max_scroll = 0

    def scroll(self, dy):
        self.scroll_y = clamp(self.scroll_y + dy, 0, max(0, self._max_scroll))

    def reset_scroll(self):
        self.scroll_y = 0

    def card_pos(self, idx):
        """Absolute (pre-scroll) position of card idx inside the grid."""
        col = idx % self.cols
        row = idx // self.cols
        x   = self.clip_rect.x + col * CARD_CW
        y   = self.clip_rect.y + row * CARD_CH - self.scroll_y
        return x, y

    def update_max_scroll(self, count):
        rows          = max(1, (count + self.cols - 1) // self.cols)
        content_h     = rows * CARD_CH
        self._max_scroll = max(0, content_h - self.clip_rect.height)

    def is_hovered(self, idx, count):
        if idx >= count:
            return False
        x, y = self.card_pos(idx)
        if not (self.clip_rect.top <= y and y + CARD_H <= self.clip_rect.bottom + CARD_H):
            return False
        mx, my = pygame.mouse.get_pos()
        return x <= mx <= x + CARD_W and y <= my <= y + CARD_H

    def inside_clip(self, pos):
        return self.clip_rect.collidepoint(pos)

    def card_at(self, pos, count):
        """Return card index under pos, or None."""
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

        total_w = len(DECK_DEFS) * DS_W + (len(DECK_DEFS) - 1) * DS_GAP
        sx      = (WIDTH - total_w) // 2
        self.rects = [pygame.Rect(sx + i * (DS_W + DS_GAP), DS_Y, DS_W, DS_H)
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
            self.hovered = next((i for i, r in enumerate(self.rects) if r.collidepoint(e.pos)), None)
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

        # Draw exit button in top-right corner
        exit_btn = pygame.Rect(WIDTH - 60, self.DS_Y - 36, 50, 28)
        rrect(self.display, BORDER, exit_btn, r=6)
        rrect(self.display, RED if exit_btn.collidepoint(pygame.mouse.get_pos()) else BORDER, 
            exit_btn, r=6, bw=1)
        ex = fs.render("ESC - Exit", True, RED if exit_btn.collidepoint(pygame.mouse.get_pos()) else MUTED)
        self.display.blit(ex, (exit_btn.x + exit_btn.w // 2 - ex.get_width() // 2, 
                        exit_btn.y + exit_btn.h // 2 - ex.get_height() // 2))

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
            self.display.blit(lb, (r.x + DS_W // 2 - lb.get_width() // 2, r.y + DS_H - 30))


# =====================
# Card Preview Panel (now rendered inside sidebar)
# =====================
class CardPreview:
    """
    Shows a card preview. Now drawn as part of the sidebar instead of a separate left panel.
    """

    # Suit symbols for suited cards
    SUIT_COLORS = {
        "Hearts": RED, "Diamonds": RED,
        "Spades": WHITE, "Clubs": WHITE,
    }
    SUIT_SYM = {"Hearts": "♥", "Diamonds": "♦", "Spades": "♠", "Clubs": "♣"}

    # Simple color tags per card type
    TYPE_COLORS = {
        "Fire": (210, 90, 40), "Water": (50, 130, 210), "Ice": (140, 210, 240),
        "Lightning": (220, 200, 50), "Shadow": (100, 60, 160), "Light": (230, 220, 160),
        "Wind": (140, 210, 160), "Earth": (140, 110, 70), "Void": (60, 40, 90),
        "Rock": (140, 120, 100), "Paper": (200, 195, 170), "Scissors": (180, 180, 180),
        "Dragon": (200, 70, 50), "Goblin": (80, 160, 80), "Knight": (160, 160, 200),
        "Archer": (130, 180, 100), "Mage": (140, 80, 200), "Shield": (100, 140, 180),
        "Rogue": (80, 80, 120), "Paladin": (220, 195, 100), "Necromancer": (100, 60, 120),
        "Berserker": (200, 80, 60), "Ranger": (90, 160, 110), "Druid": (70, 140, 90),
        "Fireball": (220, 100, 40), "Blizzard": (120, 190, 230), "Thunderstrike": (220, 210, 60),
        "Heal": (80, 200, 120), "Barrier": (100, 160, 220), "Summon": (160, 90, 200),
        "Curse": (130, 50, 130), "Bless": (220, 200, 100), "Teleport": (80, 180, 200),
        "Drain": (160, 60, 160),
    }

    def __init__(self, display, fonts):
        self.display  = display
        self.fonts    = fonts
        self.card     = None
        self.count    = 0           # copies in current deck

    def set_card(self, card, count=0):
        self.card  = card
        self.count = count

    def _accent(self, card):
        if card is None:
            return MUTED
        name = card.split(" of ")[0] if " of " in card else card
        return self.TYPE_COLORS.get(name, BLUE)

    def draw_in_sidebar(self, sx, cy, preview_w):
        """Draw the card preview inside the sidebar. Returns the new cy position."""
        if self.card is None:
            t = self.fonts["small"].render("Hover a card", True, MUTED)
            self.display.blit(t, (sx + preview_w // 2 - t.get_width() // 2, cy + 10))
            t2 = self.fonts["small"].render("to preview it", True, DIM)
            self.display.blit(t2, (sx + preview_w // 2 - t2.get_width() // 2, cy + 28))
            cy += 56
            return cy

        accent = self._accent(self.card)

        # Accent top bar
        top = pygame.Rect(sx, cy, preview_w, 5)
        pygame.draw.rect(self.display, accent, top,
                         border_top_left_radius=6, border_top_right_radius=6)
        cy += 6

        name = self.card
        fl   = self.fonts["large"]
        fn   = self.fonts["normal"]
        fs   = self.fonts["small"]
        fd   = self.fonts.get("desc", fs)

        # Suited card special rendering
        if " of " in name:
            rank, suit = name.split(" of ")
            suit_col   = self.SUIT_COLORS.get(suit, WHITE)
            sym        = self.SUIT_SYM.get(suit, "")

            rs = fl.render(rank, True, accent)
            self.display.blit(rs, (sx + preview_w // 2 - rs.get_width() // 2, cy + 4))
            cy += rs.get_height() + 4

            ss = pygame.font.Font(None, 60).render(sym, True, suit_col)
            self.display.blit(ss, (sx + preview_w // 2 - ss.get_width() // 2, cy))
            cy += ss.get_height() + 2

            st = fn.render(suit, True, MUTED)
            self.display.blit(st, (sx + preview_w // 2 - st.get_width() // 2, cy))
            cy += st.get_height() + 4
        else:
            # Regular card
            ns = fl.render(name, True, WHITE)
            if ns.get_width() > preview_w:
                ns = fn.render(name, True, WHITE)
            self.display.blit(ns, (sx + preview_w // 2 - ns.get_width() // 2, cy + 4))
            cy += ns.get_height() + 6

            # Type indicator dot
            pygame.draw.circle(self.display, accent, (sx + preview_w // 2, cy + 14), 18)
            pygame.draw.circle(self.display, PANEL2, (sx + preview_w // 2, cy + 14), 16)
            pygame.draw.circle(self.display, accent, (sx + preview_w // 2, cy + 14), 10)
            cy += 32

        # In-deck count
        if self.count > 0:
            ct = fn.render(f"×{self.count} in deck", True, TEAL)
            self.display.blit(ct, (sx + preview_w // 2 - ct.get_width() // 2, cy))
        else:
            ct = fs.render("not in deck", True, MUTED)
            self.display.blit(ct, (sx + preview_w // 2 - ct.get_width() // 2, cy))
        cy += ct.get_height() + 6

        # Divider
        pygame.draw.line(self.display, BORDER,
                         (sx + 4, cy), (sx + preview_w - 4, cy), 1)
        cy += 6

        # Flavour type label
        if " of " in self.card:
            type_label = "Suited"
        elif self.card in ["Fireball","Blizzard","Thunderstrike","Heal",
                           "Barrier","Summon","Curse","Bless","Teleport","Drain"]:
            type_label = "Spell"
        elif self.card in ["Rock","Paper","Scissors","Fire","Water","Wind",
                           "Earth","Lightning","Ice","Shadow","Light","Void"]:
            type_label = "Element"
        else:
            type_label = "Unit"

        tl = fs.render(type_label.upper(), True, accent)
        self.display.blit(tl, (sx + preview_w // 2 - tl.get_width() // 2, cy))
        cy += tl.get_height() + 6

        # Description
        desc = CARD_DESCRIPTIONS.get(self.card, "A mysterious card with unknown properties.")
        desc_lines = wrap_text(fd, desc, preview_w - 8)
        for line in desc_lines:
            ds = fd.render(line, True, MUTED)
            self.display.blit(ds, (sx + 4, cy))
            cy += ds.get_height() + 2
        cy += 4

        # Divider
        pygame.draw.line(self.display, BORDER,
                         (sx + 4, cy), (sx + preview_w - 4, cy), 1)
        cy += 8

        return cy


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
            "mono":   pygame.font.Font(None, 20),
            "desc":   pygame.font.Font(None, 19),
        }

        self.collection  = list(ALL_CARDS)
        self.owned_cards = {c: 2 for c in self.collection}

        self.decks       = [{}, {}, {}]
        self.active_deck = 0
        self.undo_stacks = [[], [], []]
        self.unsaved     = [False, False, False]

        self.dragging_card  = None
        self.drag_from      = None
        self.drag_pos       = (0, 0)
        self.last_card      = None   # last hovered/touched card for preview

        self.status       = ""
        self.status_timer = 0

        # ---- Layout -------------------------------------------------
        # Preview panel (now rendered inside sidebar, no separate rect)
        self.preview = CardPreview(display, self.fonts)

        # Deck grid clip rect (now uses full width)
        deck_clip = pygame.Rect(DECK_PANEL_X, DECK_Y, DECK_PANEL_W, DECK_VIS_H)
        self.deck_grid = CardGrid(display, deck_clip, cols=CARD_COLS)

        # Collection grid clip rect (now uses full width)
        coll_clip = pygame.Rect(COLL_PANEL_X, COLL_Y, COLL_PANEL_W, COLL_VIS_H)
        self.coll_grid = CardGrid(display, coll_clip, cols=CARD_COLS)

        # Deck selector
        self.selector = DeckSelector(display, self.fonts)

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
                        # Support multi-word card names: "Ace of Spades x1"
                        m = re.match(r"^(.+?)\s+x(\d+)$", line)
                        if m:
                            card, count = m.group(1).strip(), int(m.group(2))
                            if card in self.collection:
                                self.decks[current_idx][card] = count
            self.unsaved = [False, False, False]
            self.set_status("Loaded from file")
        except Exception as e:
            self.set_status(f"Load error: {e}")

    def save_deck(self):
        lines = []
        for i, d in enumerate(DECK_DEFS):
            lines.append(f"[{d['label']}]")
            dk = self.decks[i]
            for card, count in sorted(dk.items()):
                lines.append(f"  {card} x{count}")
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
                if e.button == 3:
                    self._right_click(e.pos)
                elif e.button == 1:
                    self.start_drag(e.pos)

            elif e.type == pygame.MOUSEBUTTONUP:
                if e.button == 1:
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

        return True

    def _update_preview_hover(self, pos):
        """Update preview card based on mouse position."""
        # Check collection
        for i, card in enumerate(self.collection):
            cx, cy = self.coll_grid.card_pos(i)
            if cx <= pos[0] <= cx + CARD_W and cy <= pos[1] <= cy + CARD_H:
                if self.coll_grid.clip_rect.collidepoint(pos):
                    self.preview.set_card(card, self.deck.get(card, 0))
                    return
        # Check deck
        deck_list = self.expand_deck()
        for i, card in enumerate(deck_list):
            cx, cy = self.deck_grid.card_pos(i)
            if cx <= pos[0] <= cx + CARD_W and cy <= pos[1] <= cy + CARD_H:
                if self.deck_grid.clip_rect.collidepoint(pos):
                    self.preview.set_card(card, self.deck.get(card, 0))
                    return

    def _switch_deck(self, idx):
        self.active_deck = idx
        self.deck_grid.reset_scroll()
        self.set_status(f"Switched to {self.deck_name()}")

    # =====================
    # Interactions
    # =====================
    def _right_click(self, pos):
        # Collection
        idx = self.coll_grid.card_at(pos, len(self.collection))
        if idx is not None:
            card = self.collection[idx]
            if self.total_cards() >= MAX_DECK:
                self.set_status("Deck Full!")
            elif self.copies_avail(card) <= 0:
                self.set_status("No copies left!")
            else:
                self.push_undo()
                self.add_card(card)
                self.preview.set_card(card, self.deck.get(card, 0))
                self.set_status(f"Added {card}")
            return
        # Deck
        deck_list = self.expand_deck()
        idx = self.deck_grid.card_at(pos, len(deck_list))
        if idx is not None:
            self.remove_card(deck_list[idx])

    def start_drag(self, pos):
        # From collection
        idx = self.coll_grid.card_at(pos, len(self.collection))
        if idx is not None:
            card = self.collection[idx]
            if self.copies_avail(card) > 0:
                self.dragging_card = card
                self.drag_from     = "collection"
                self.preview.set_card(card, self.deck.get(card, 0))
            else:
                self.set_status("No copies left!")
            return
        # From deck
        deck_list = self.expand_deck()
        idx = self.deck_grid.card_at(pos, len(deck_list))
        if idx is not None:
            self.dragging_card = deck_list[idx]
            self.drag_from     = "deck"
            self.push_undo()
            self.deck[deck_list[idx]] -= 1
            if self.deck[deck_list[idx]] <= 0:
                del self.deck[deck_list[idx]]
            self.preview.set_card(self.dragging_card, self.deck.get(self.dragging_card, 0))

    def end_drag(self, pos):
        if not self.dragging_card:
            return
        in_deck = self.deck_grid.clip_rect.collidepoint(pos)

        if in_deck:
            if self.total_cards() >= MAX_DECK:
                self.set_status("Deck Full!")
                if self.drag_from == "deck":
                    self.deck[self.dragging_card] = self.deck.get(self.dragging_card, 0) + 1
            else:
                if self.drag_from == "collection":
                    self.push_undo()
                self.add_card(self.dragging_card)
                self.preview.set_card(self.dragging_card, self.deck.get(self.dragging_card, 0))
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
    def add_card(self, card):
        self.deck[card] = self.deck.get(card, 0) + 1
        self.unsaved[self.active_deck] = True

    def remove_card(self, card):
        if card and card in self.deck:
            self.push_undo()
            self.deck[card] -= 1
            if self.deck[card] <= 0:
                del self.deck[card]
            self.unsaved[self.active_deck] = True
            self.set_status(f"Removed {card}")

    def clear_deck(self):
        if self.deck:
            self.push_undo()
            self.deck = {}
            self.unsaved[self.active_deck] = True
            self.set_status("Deck Cleared!")

    def expand_deck(self):
        r = []
        for card, count in self.deck.items():
            r.extend([card] * count)
        return r

    def total_cards(self):
        return sum(self.deck.values())

    def copies_avail(self, card):
        return self.owned_cards.get(card, 0) - self.deck.get(card, 0)

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

    def draw_card_widget(self, card, pos, in_deck=False, greyed=False):
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

        # Accent stripe at top using card type colour
        name_key = card.split(" of ")[0] if " of " in card else card
        accent   = CardPreview.TYPE_COLORS.get(name_key, BLUE)
        stripe   = pygame.Rect(rx + 1, ry + 1, CARD_W - 2, 4)
        pygame.draw.rect(self.display, accent, stripe,
                         border_top_left_radius=6, border_top_right_radius=6)

        # Suit symbol for suited cards
        if " of " in card:
            rank, suit = card.split(" of ")
            sym_col = CardPreview.SUIT_COLORS.get(suit, WHITE)
            sym     = CardPreview.SUIT_SYM.get(suit, "")
            ss      = pygame.font.Font(None, 28).render(sym, True, sym_col)
            self.display.blit(ss, (rx + 4, ry + 8))
            ns = self.fonts["small"].render(rank, True, WHITE if not greyed else MUTED)
            self.display.blit(ns, (rx + CARD_W // 2 - ns.get_width() // 2, ry + 60))
            su = self.fonts["small"].render(suit, True, MUTED)
            self.display.blit(su, (rx + CARD_W // 2 - su.get_width() // 2, ry + 78))
        else:
            ns = self.fonts["normal"].render(card, True, WHITE if not greyed else MUTED)
            # Wrap long names
            if ns.get_width() > CARD_W - 8:
                ns = self.fonts["small"].render(card, True, WHITE if not greyed else MUTED)
            self.display.blit(ns, (rx + CARD_W // 2 - ns.get_width() // 2, ry + 62))

        # Stack badge
        if in_deck and card in self.deck and self.deck[card] > 1:
            br = pygame.Rect(rx + CARD_W - 26, ry + 5, 22, 18)
            rrect(self.display, (160, 50, 50), br, r=4)
            bt = self.fonts["small"].render(f"×{self.deck[card]}", True, WHITE)
            self.display.blit(bt, (br.x + 1, br.y + 1))

    def draw_scrollbar(self, grid, total_rows):
        r         = grid.clip_rect
        vis_rows  = r.height / CARD_CH
        if total_rows <= vis_rows:
            return
        track = pygame.Rect(r.right + 3, r.top, 4, r.height)
        rrect(self.display, PANEL2, track, r=2)
        ratio  = vis_rows / total_rows
        thumb_h = max(20, int(r.height * ratio))
        frac    = grid.scroll_y / max(1, grid._max_scroll)
        thumb_y = r.top + int((r.height - thumb_h) * frac)
        thumb   = pygame.Rect(r.right + 3, thumb_y, 4, thumb_h)
        rrect(self.display, TEAL, thumb, r=2)

    def draw_deck_area(self):
        deck_list = self.expand_deck()
        self.deck_grid.update_max_scroll(len(deck_list))

        # Panel
        panel_r = pygame.Rect(DECK_PANEL_X - PAD, DECK_LABEL_Y - 4,
                              DECK_PANEL_W + PAD + 12, DECK_VIS_H + 34)
        panel(self.display, panel_r, r=10)

        # Label row
        lx, ly = DECK_PANEL_X, DECK_LABEL_Y
        self._txt("DECK", lx, ly, MUTED, "small")
        cc = RED if self.total_cards() >= MAX_DECK else TEAL
        self._txt(f"{self.total_cards()}/{MAX_DECK}", lx + 48, ly, cc, "small")
        if self.unsaved[self.active_deck]:
            self._txt("● unsaved", lx + 110, ly, AMBER, "small")

        # Scroll hint
        if self.deck_grid._max_scroll > 0:
            self._txt("scroll ↕", panel_r.right - 68, ly, DIM, "small")

        # Draw cards inside clip
        self.deck_grid.draw_clip_start()
        for i, card in enumerate(deck_list):
            pos = self.deck_grid.card_pos(i)
            if self.deck_grid.clip_rect.top - CARD_H <= pos[1] <= self.deck_grid.clip_rect.bottom:
                self.draw_card_widget(card, pos, in_deck=True)
        self.deck_grid.draw_clip_end()

        self.draw_scrollbar(self.deck_grid,
                            max(1, (len(deck_list) + CARD_COLS - 1) // CARD_COLS))

    def draw_collection_area(self):
        self.coll_grid.update_max_scroll(len(self.collection))

        panel_r = pygame.Rect(COLL_PANEL_X - PAD, COLL_LABEL_Y - 4,
                              COLL_PANEL_W + PAD + 12, COLL_VIS_H + 34)
        panel(self.display, panel_r, r=10)

        lx, ly = COLL_PANEL_X, COLL_LABEL_Y
        self._txt("COLLECTION", lx, ly, MUTED, "small")
        self._txt(f"{len(self.collection)} cards", lx + 92, ly, MUTED, "small")
        if self.coll_grid._max_scroll > 0:
            self._txt("scroll ↕", panel_r.right - 68, ly, DIM, "small")

        self.coll_grid.draw_clip_start()
        for i, card in enumerate(self.collection):
            pos   = self.coll_grid.card_pos(i)
            avail = self.copies_avail(card)
            owned = self.owned_cards.get(card, 0)
            ind   = self.deck.get(card, 0)
            if self.coll_grid.clip_rect.top - CARD_H <= pos[1] <= self.coll_grid.clip_rect.bottom:
                self.draw_card_widget(card, pos, in_deck=False, greyed=avail <= 0)
                # copies count below card name
                cc  = RED if ind >= owned else MUTED
                ct  = self.fonts["small"].render(f"{ind}/{owned}", True, cc)
                self.display.blit(ct, (pos[0] + CARD_W // 2 - ct.get_width() // 2,
                                       pos[1] + CARD_H - 19))
        self.coll_grid.draw_clip_end()

        self.draw_scrollbar(self.coll_grid,
                            max(1, (len(self.collection) + CARD_COLS - 1) // CARD_COLS))

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

        cy = 90
        preview_w = sw - 30

        # --- Card Preview (moved here from left panel) ---
        cy = self.preview.draw_in_sidebar(sx + 6, cy, preview_w)

        # --- Controls ---
        controls = [
            ("ESC", "Main menu"),
            ("V",   "View cards"),
            ("D",   "Choose deck"),
            ("S",   "Save"),
            ("Z",   "Undo"),
            ("C",   "Clear"),
            ("G",   "Generate Hand"),
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

        hints = [("RMB coll.", "add"), ("RMB deck", "remove"), ("Drag", "add")]
        for lbl, act in hints:
            if cy + 22 > HEIGHT - 10:
                break
            self._txt(f"{lbl} → {act}", sx + 6, cy, DIM, "small")
            cy += 22

        if cy + 10 < HEIGHT:
            pygame.draw.line(self.display, BORDER, (sx, cy + 2), (WIDTH - 4, cy + 2), 1)
            cy += 10

        if cy + 20 < HEIGHT:
            self._txt("Stats", sx + 6, cy, WHITE, "small"); cy += 20
        if cy + 20 < HEIGHT:
            self._txt(f"Unique  {len(self.deck)}", sx + 6, cy, MUTED, "small"); cy += 20
        if cy + 20 < HEIGHT:
            self._txt(f"Total   {self.total_cards()}/{MAX_DECK}", sx + 6, cy, MUTED, "small"); cy += 20
        if cy + 20 < HEIGHT:
            self._txt(f"Undos   {len(self.undo_stack)}", sx + 6, cy, MUTED, "small"); cy += 20

        if cy + 10 < HEIGHT:
            pygame.draw.line(self.display, BORDER, (sx, cy + 2), (WIDTH - 4, cy + 2), 1)
            cy += 10

        if self.status and cy + 20 < HEIGHT:
            col = (GREEN  if any(w in self.status for w in ("Saved","Added","Loaded","Switched"))
                   else RED    if any(w in self.status for w in ("Full","error","No"))
                   else WHITE)
            self._txt(self.status, sx + 6, cy, col, "normal")

    def draw_drag_ghost(self):
        if not self.dragging_card:
            return
        dx = self.drag_pos[0] - CARD_W // 2
        dy = self.drag_pos[1] - CARD_H // 2
        ghost = pygame.Surface((CARD_W, CARD_H), pygame.SRCALPHA)
        pygame.draw.rect(ghost, (*BLUE, 170), (0, 0, CARD_W, CARD_H), border_radius=7)
        pygame.draw.rect(ghost, (*WHITE, 220), (0, 0, CARD_W, CARD_H), 1, border_radius=7)
        self.display.blit(ghost, (dx, dy))
        s = self.fonts["normal"].render(self.dragging_card, True, WHITE)
        self.display.blit(s, (dx + CARD_W // 2 - s.get_width() // 2, dy + 58))

    def draw(self):
        self.tick_status()
        self.display.fill(BG)

        self.draw_tabs()
        self.draw_deck_area()
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