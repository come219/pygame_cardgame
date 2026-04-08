import pygame
import sys

# Try to import cardgame for navigation
try:
    import cardgame
    HAS_CARDGAME = True
except ImportError:
    HAS_CARDGAME = False

# Try to import deck_manager for navigation
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
# Palette  (matching deck_viewer dark slate / teal accent)
# =====================
BG            = (12,  14,  20)
PANEL         = (20,  24,  34)
PANEL2        = (26,  30,  42)
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

# =====================
# Layout
# =====================
PAD          = 14
SIDEBAR_X    = 1490
SIDEBAR_W    = WIDTH - SIDEBAR_X + 8
CARD_W       = 150
CARD_H       = 150
CARD_GAP     = 10
CARD_CW      = CARD_W + CARD_GAP
CARD_CH      = CARD_H + CARD_GAP
COLS         = 9
STATUS_DUR   = 180

# Grid now starts from the left edge (no left preview panel)
GRID_X       = PAD
GRID_Y       = 60
GRID_W       = SIDEBAR_X - GRID_X - PAD
GRID_H       = HEIGHT - GRID_Y - 60

# =====================
# Card categories / image paths
# =====================
CARD_CATALOG = [
    # --- Core Elements ---
    {"name": "Rock",            "image": "assets/card_rock.png",            "category": "Core", "desc": "The classic. Strong against Scissors and Lizard, weak to Paper and Spock."},
    {"name": "Paper",           "image": "assets/card_paper.png",           "category": "Core", "desc": "Covers Rock and disproves Spock. Weak to Scissors and Lizard."},
    {"name": "Scissors",        "image": "assets/card_scissors.png",        "category": "Core", "desc": "Cuts Paper and decapitates Lizard. Weak to Rock and Spock."},
    {"name": "Snake",           "image": "assets/card_snake.png",           "category": "Core", "desc": "A slithering predator. Strikes swiftly and poisons its foes."},
    {"name": "Human",           "image": "assets/card_human.png",           "category": "Core", "desc": "The adaptable species. Uses tools and cunning to overcome obstacles."},
    {"name": "Dragon",          "image": "assets/card_dragon.png",          "category": "Core", "desc": "A mighty beast of fire and fury. Dominates the skies with raw power."},
    {"name": "Wolf",            "image": "assets/card_wolf.png",            "category": "Core", "desc": "Pack hunter with sharp instincts. Overwhelms foes through teamwork."},
    {"name": "Devil",           "image": "assets/card_devil.png",           "category": "Core", "desc": "A dark entity of chaos. Corrupts and undermines all who oppose it."},
    {"name": "Lightning",       "image": "assets/card_lightning.png",       "category": "Core", "desc": "Pure electrical energy. Strikes fast and leaves devastation in its wake."},
    {"name": "Gun",             "image": "assets/card_gun.png",             "category": "Core", "desc": "Modern firepower. Delivers precise, ranged damage to any target."},
    {"name": "Fire",            "image": "assets/card_fire.png",            "category": "Core", "desc": "Primal element of destruction. Burns through organic matter with ease."},
    {"name": "Water",           "image": "assets/card_water.png",           "category": "Core", "desc": "The life-giving element. Extinguishes fire and erodes stone over time."},
    {"name": "Air",             "image": "assets/card_air.png",             "category": "Core", "desc": "Invisible but powerful. Fuels fire and carries storms across the land."},
    {"name": "Sponge",          "image": "assets/card_sponge.png",          "category": "Core", "desc": "Absorbent and resilient. Soaks up water and smothers fire."},
    {"name": "Tree",            "image": "assets/card_tree.png",            "category": "Core", "desc": "Rooted and enduring. Draws strength from earth and shelters life."},
    {"name": "Lizard",          "image": "assets/card_lizard.png",          "category": "Core", "desc": "Poisons Spock and eats Paper. A cunning reptilian survivor."},
    {"name": "Spock",           "image": "assets/card_spock.png",           "category": "Core", "desc": "Smashes Scissors and vaporizes Rock. Logic is his greatest weapon."},
    {"name": "Earth",           "image": "assets/card_earth.png",           "category": "Core", "desc": "The foundation of all. Immovable and enduring against most forces."},
    {"name": "Metal",           "image": "assets/card_metal.png",           "category": "Core", "desc": "Forged and unyielding. Resists blows and conducts lightning."},
    {"name": "Bear",            "image": "assets/card_bear.png",            "category": "Core", "desc": "Raw brute strength. Overpowers most creatures in close combat."},
    {"name": "Computer",        "image": "assets/card_computer.png",        "category": "Core", "desc": "Calculates optimal strategies. Outthinks opponents with pure logic."},
    {"name": "Balance",         "image": "assets/card_balance.png",         "category": "Core", "desc": "Restores equilibrium. Neutralizes extreme advantages on either side."},
    {"name": "Void",            "image": "assets/card_void.png",            "category": "Core", "desc": "The absence of everything. Consumes matter and energy alike."},
    {"name": "Super Paper",     "image": "assets/card_super_paper.png",     "category": "Core", "desc": "An enhanced version of Paper with amplified covering power."},
    {"name": "Skissors",        "image": "assets/card_skissors.png",        "category": "Core", "desc": "A twisted variant of Scissors. Unpredictable and dangerously sharp."},
    # --- Toon ---
    {"name": "Toon Spock",      "image": "assets/card_toon_spock.png",      "category": "Toon", "desc": "A cartoonish Spock. Same logic, but with a playful twist."},
    {"name": "Toon Snake",      "image": "assets/card_toon_snake.png",      "category": "Toon", "desc": "A goofy serpent from Toon World. Silly but still venomous."},
    {"name": "Toon Lizard",     "image": "assets/card_toon_lizard.png",     "category": "Toon", "desc": "A comical lizard with big eyes. Don't underestimate its bite."},
    {"name": "Toon Metal",      "image": "assets/card_toon_metal.png",      "category": "Toon", "desc": "Shiny cartoon metal. Bounces attacks back with a comedic clang."},
    {"name": "Toon Angel",      "image": "assets/card_toon_angel.png",      "category": "Toon", "desc": "A whimsical angel from Toon World. Heals allies with cartoon magic."},
    {"name": "Toon Fire",       "image": "assets/card_toon_fire.png",       "category": "Toon", "desc": "Animated flames that dance and giggle. Still burns, though!"},
    {"name": "Toon Water",      "image": "assets/card_toon_water.png",      "category": "Toon", "desc": "A bubbly splash of cartoon water. Playful but effective."},
    {"name": "Toon Earth",      "image": "assets/card_toon_earth.png",      "category": "Toon", "desc": "A bouncy cartoon planet. Surprisingly heavy when it lands on you."},
    {"name": "Toon Dragon",     "image": "assets/card_toon_dragon.png",     "category": "Toon", "desc": "A cute but fierce cartoon dragon. Breathes rainbow fire."},
    {"name": "Toon Gun",        "image": "assets/card_toon_gun.png",        "category": "Toon", "desc": "A toy-like gun that shoots cork bullets. Comedic but startling."},
    {"name": "Toon T.O.C.",     "image": "assets/card_toon_table_of_contents.png", "category": "Toon", "desc": "Table of Contents for Toon World. Organizes all toon cards."},
    {"name": "Toon Bookmark",   "image": "assets/card_toon_bookmark.png",   "category": "Toon", "desc": "Marks a page in Toon World. Lets you return to a saved state."},
    {"name": "Toon World",      "image": "assets/card_toon_world.png",      "category": "Toon", "desc": "The magical storybook realm. All Toon cards gain power here."},
    {"name": "Toon Kingdom",    "image": "assets/card_toon_kingdom.png",    "category": "Toon", "desc": "An upgraded Toon World. Protects Toon monsters from destruction."},
    # --- Special / Rule Cards ---
    {"name": "No Lose",         "image": "assets/card_no_lose.png",         "category": "Special", "desc": "Prevents you from losing this round. A powerful safety net."},
    {"name": "Stop Card",       "image": "assets/card_stop_card.png",       "category": "Special", "desc": "Halts the opponent's action for one turn. Buys precious time."},
    {"name": "Counter Stop",    "image": "assets/card_counter_stop.png",    "category": "Special", "desc": "Negates a Stop Card. Keeps your momentum going."},
    {"name": "Fundamentals",    "image": "assets/card_fundamentals_only.png","category": "Special", "desc": "Restricts play to core elements only. Strips away all extras."},
    {"name": "Non-Core",        "image": "assets/card_non_core.png",         "category": "Special", "desc": "Allows only non-core cards to be played this round."},
    {"name": "Reload",          "image": "assets/card_reload.png",           "category": "Special", "desc": "Refreshes your hand. Draw new cards to replace current ones."},
    {"name": "Magical Mallet",  "image": "assets/card_magical_mallet.png",   "category": "Special", "desc": "Shuffle chosen cards back into the deck and draw the same number."},
    {"name": "Jar of Greed",    "image": "assets/card_jar_of_greed.png",     "category": "Special", "desc": "Draw one extra card from your deck. Simple but effective."},
    # --- Exodia ---
    {"name": "Exodia",          "image": "assets/card_exodia_the_forbidden_one.png", "category": "Exodia", "desc": "The Forbidden One. Collect all pieces to achieve an instant victory."},
    {"name": "Full Exodia",     "image": "assets/card_full_exodia.png",      "category": "Exodia", "desc": "The complete Exodia assembled. Unleashes unstoppable obliteration."},
    {"name": "Left Arm",        "image": "assets/card_left_arm_of_exodia.png","category": "Exodia", "desc": "Left Arm of the Forbidden One. One of five pieces needed for Exodia."},
    {"name": "Right Arm",       "image": "assets/card_right_arm_of_exodia.png","category": "Exodia", "desc": "Right Arm of the Forbidden One. One of five pieces needed for Exodia."},
    {"name": "Left Leg",        "image": "assets/card_left_leg_of_exodia.png","category": "Exodia", "desc": "Left Leg of the Forbidden One. One of five pieces needed for Exodia."},
    {"name": "Right Leg",       "image": "assets/card_right_leg_of_exodia.png","category": "Exodia", "desc": "Right Leg of the Forbidden One. One of five pieces needed for Exodia."},
    {"name": "Tassets",         "image": "assets/card_tassets_of_exodia.png", "category": "Exodia", "desc": "Tassets of Exodia. Protective armor piece of the Forbidden One."},
    {"name": "Shadow Exodia",   "image": "assets/card_shadow_of_exodia.png",  "category": "Exodia", "desc": "A dark reflection of Exodia. Mimics the Forbidden One's power."},
    {"name": "Stop Exodia",     "image": "assets/card_stop_exodia.png",       "category": "Exodia", "desc": "Prevents Exodia from being summoned. The ultimate counter."},
    {"name": "Pot of Greed",    "image": "assets/card_pot_of_greed.png",      "category": "Exodia", "desc": "Draw two additional cards. A staple for any Exodia strategy."},
    # --- Holy / Units ---
    {"name": "Holy Knight",     "image": "assets/card_holy_knight.png",      "category": "Units", "desc": "A divine warrior clad in blessed armor. Strikes with holy fury."},
    {"name": "Holy Archer",     "image": "assets/card_holy_archer.png",      "category": "Units", "desc": "A sacred marksman. Fires arrows of light at distant foes."},
    {"name": "Holy Mage",       "image": "assets/card_holy_mage.png",        "category": "Units", "desc": "A priest of arcane power. Casts healing and offensive miracles."},
    {"name": "Castle",          "image": "assets/card_castle.png",           "category": "Units", "desc": "A fortified stronghold. Provides defense and rallies nearby units."},
    {"name": "Keep",            "image": "assets/card_keep.png",             "category": "Units", "desc": "The inner fortress. Last line of defense with reinforced walls."},
    {"name": "Footman",         "image": "assets/card_footman.png",          "category": "Units", "desc": "A reliable infantry soldier. Holds the front line with shield and sword."},
    {"name": "Rifleman",        "image": "assets/card_rifleman.png",         "category": "Units", "desc": "A ranged combatant with a rifle. Picks off enemies from a distance."},
    {"name": "Knight",          "image": "assets/card_knight.png",           "category": "Units", "desc": "A mounted warrior. Charges into battle with devastating momentum."},
    {"name": "Stronghold",      "image": "assets/card_stronghold.png",       "category": "Units", "desc": "A massive fortification. Nearly impenetrable and boosts garrison morale."},
    {"name": "Grunt",           "image": "assets/card_grunt.png",            "category": "Units", "desc": "A basic but fierce orc warrior. Fights with raw aggression."},
    {"name": "Burrow",          "image": "assets/card_burrow.png",           "category": "Units", "desc": "An underground hideout. Conceals units and enables surprise attacks."},
    {"name": "Ghoul",           "image": "assets/card_ghoul.png",            "category": "Units", "desc": "An undead scavenger. Regenerates health by consuming fallen foes."},
    {"name": "Blue Eyes Dragon","image": "assets/card_blue_eyes_white_dragon.png","category": "Units", "desc": "The legendary Blue-Eyes White Dragon. Devastating burst stream of destruction."},
    {"name": "Red Eyes Dragon", "image": "assets/card_red_eyes_black_dragon.png", "category": "Units", "desc": "The fierce Red-Eyes Black Dragon. Inferno fire blast incinerates all."},
    {"name": "Moon Champion",   "image": "assets/card_moon_champion.png",    "category": "Units", "desc": "A warrior empowered by moonlight. Grows stronger as night falls."},
    {"name": "Lunar Soldier",   "image": "assets/card_soldier_of_lunar_light.png","category": "Units", "desc": "A soldier blessed by the moon. Fights with ethereal lunar energy."},
    {"name": "Void Bard",       "image": "assets/card_void_bard.png",        "category": "Units", "desc": "A musician of the void. Plays haunting melodies that weaken enemies."},
    # --- Spells / Traps ---
    {"name": "Trap Stun",       "image": "assets/card_trap_stun.png",        "category": "Spells", "desc": "Negates all trap cards for this turn. Clears the way for your play."},
    {"name": "Barbed Armour",   "image": "assets/card_barbed_armour.png",    "category": "Spells", "desc": "Reflects a portion of damage back to the attacker. Punishes aggression."},
    {"name": "Swords of Hope",  "image": "assets/swords_of_hope_card.png",   "category": "Spells", "desc": "Protective swords that shield you. Stalls the opponent for multiple turns."},
    {"name": "Whip",            "image": "assets/whip_card.png",             "category": "Spells", "desc": "A swift lashing attack. Deals damage and reduces enemy defense."},
    {"name": "Silence",         "image": "assets/silence_card.png",          "category": "Spells", "desc": "Mutes the opponent's special abilities for one turn. Pure suppression."},
    {"name": "Greater Axe",     "image": "assets/greater_axe_card.png",      "category": "Spells", "desc": "A massive enchanted axe. Boosts attack power significantly."},
    {"name": "Black Hole",      "image": "assets/blackhole_card.png",        "category": "Spells", "desc": "Destroys all cards on the field. A devastating reset for both sides."},
    {"name": "Mystical Typhoon","image": "assets/mysticalspacetypoon_card.png","category": "Spells", "desc": "Destroys one spell or trap card on the field. Precise removal."},
    # --- AA (Action Arena) ---
    {"name": "AA Shoot",        "image": "assets/card_aa_shoot.png",         "category": "AA", "desc": "Fire your weapon in the Action Arena. Deals direct damage."},
    {"name": "AA Reload",       "image": "assets/card_aa_reload.png",        "category": "AA", "desc": "Reload your ammunition. Required before you can shoot again."},
    {"name": "AA Block",        "image": "assets/card_aa_block.png",         "category": "AA", "desc": "Raise your shield to block an incoming shot. Negates damage."},
    {"name": "AA Can't Shoot",  "image": "assets/card_aa_cant_shoot.png",    "category": "AA", "desc": "Prevents the opponent from shooting next turn. Tactical denial."},
    {"name": "AA Reflect Shot", "image": "assets/card_aa_reflect_shot.png",  "category": "AA", "desc": "Reflects an incoming shot back at the attacker. Risky but rewarding."},
    {"name": "AA Extra Heart",  "image": "assets/card_aa_extra_heart.png",   "category": "AA", "desc": "Grants one additional life point. Extends your survival in the arena."},
    {"name": "AA Reset",        "image": "assets/card_aa_reset_players.png", "category": "AA", "desc": "Resets both players to their starting state. A full arena restart."},
]

CATEGORIES = ["All", "Core", "Toon", "Special", "Exodia", "Units", "Spells", "AA"]

CATEGORY_COLORS = {
    "All":     BLUE,
    "Core":    TEAL,
    "Toon":    PURPLE,
    "Special": AMBER,
    "Exodia":  RED,
    "Units":   (75, 175, 120),
    "Spells":  (180, 100, 220),
    "AA":      (220, 140, 60),
}


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
    """Word-wrap text to fit within max_width. Returns list of lines."""
    words = text.split(' ')
    lines = []
    current_line = ""
    for word in words:
        test = current_line + (" " if current_line else "") + word
        if font.size(test)[0] <= max_width:
            current_line = test
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines


# =====================
# Image Cache
# =====================
_img_cache = {}

def load_image(path, w, h):
    key = (path, w, h)
    if key in _img_cache:
        return _img_cache[key]
    try:
        img = pygame.image.load(path).convert_alpha()
        img = pygame.transform.smoothscale(img, (w, h))
        _img_cache[key] = img
    except Exception:
        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        surf.fill((40, 40, 60, 200))
        _img_cache[key] = surf
    return _img_cache[key]


# =====================
# Scrollable Grid
# =====================
class CardGrid:
    def __init__(self, display, clip_rect, cols=COLS):
        self.display   = display
        self.clip_rect = clip_rect
        self.cols      = cols
        self.scroll_y  = 0
        self._max_scroll = 0

    def scroll(self, dy):
        self.scroll_y = clamp(self.scroll_y + dy, 0, max(0, self._max_scroll))

    def reset_scroll(self):
        self.scroll_y = 0

    def card_pos(self, idx):
        col = idx % self.cols
        row = idx // self.cols
        x   = self.clip_rect.x + col * CARD_CW
        y   = self.clip_rect.y + row * CARD_CH - self.scroll_y
        return x, y

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
# Card Viewer App
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
        }

        self.all_cards     = list(CARD_CATALOG)
        self.active_cat    = "All"
        self.filtered      = list(self.all_cards)
        self.selected_card = None

        self.status       = ""
        self.status_timer = 0

        # Sidebar scroll for preview overflow
        self.sidebar_scroll_y = 0
        self._sidebar_max_scroll = 0

        # Grid clip region (now starts from left edge, no left preview panel)
        grid_clip = pygame.Rect(GRID_X, GRID_Y + 50, GRID_W, GRID_H - 50)
        self.grid = CardGrid(display, grid_clip, cols=COLS)

        # Category tab rects
        self._build_cat_tabs()

    def _build_cat_tabs(self):
        tab_w  = 110
        tab_h  = 34
        tab_gap = 6
        start_x = GRID_X
        self.cat_tabs = {}
        for i, cat in enumerate(CATEGORIES):
            rx = start_x + i * (tab_w + tab_gap)
            self.cat_tabs[cat] = pygame.Rect(rx, GRID_Y + 8, tab_w, tab_h)

    def set_category(self, cat):
        self.active_cat = cat
        if cat == "All":
            self.filtered = list(self.all_cards)
        else:
            self.filtered = [c for c in self.all_cards if c["category"] == cat]
        self.grid.reset_scroll()
        self.set_status(f"{cat}  ·  {len(self.filtered)} cards")

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
                # Check if mouse is over sidebar for sidebar scrolling
                sidebar_rect = pygame.Rect(SIDEBAR_X - 8, 0, SIDEBAR_W, HEIGHT)
                if sidebar_rect.collidepoint(mx, my):
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
                        self.set_category(cat)
                        break
                else:
                    # Card click
                    idx = self.grid.card_at(pos, len(self.filtered))
                    if idx is not None:
                        self.selected_card = self.filtered[idx]
                        self.sidebar_scroll_y = 0
                        self.set_status(f"Viewing: {self.selected_card['name']}")

            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    if HAS_CARDGAME:
                        cardgame.main()
                    return False
                elif e.key == pygame.K_d:
                    if HAS_DECK_MANAGER:
                        deck_manager.main()
                    return False
                elif e.key == pygame.K_r:
                    self.selected_card = None
                    self.set_category("All")
                    self.set_status("Reset")
                elif e.key == pygame.K_LEFT:
                    cats = CATEGORIES
                    idx  = cats.index(self.active_cat)
                    self.set_category(cats[(idx - 1) % len(cats)])
                elif e.key == pygame.K_RIGHT:
                    cats = CATEGORIES
                    idx  = cats.index(self.active_cat)
                    self.set_category(cats[(idx + 1) % len(cats)])
                # Number keys: quick jump to categories
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
        r        = self.grid.clip_rect
        count    = len(self.filtered)
        total_rows = max(1, (count + COLS - 1) // COLS)
        vis_rows   = r.height / CARD_CH
        if total_rows <= vis_rows:
            return
        track = pygame.Rect(r.right + 4, r.top, 5, r.height)
        rrect(self.display, PANEL2, track, r=2)
        ratio   = vis_rows / total_rows
        thumb_h = max(20, int(r.height * ratio))
        frac    = self.grid.scroll_y / max(1, self.grid._max_scroll)
        thumb_y = r.top + int((r.height - thumb_h) * frac)
        thumb   = pygame.Rect(r.right + 4, thumb_y, 5, thumb_h)
        rrect(self.display, TEAL, thumb, r=2)

    def draw_category_tabs(self):
        for cat, rect in self.cat_tabs.items():
            active = (cat == self.active_cat)
            col    = CATEGORY_COLORS.get(cat, BLUE)
            bg     = (28, 40, 60) if active else PANEL
            bord   = col if active else BORDER
            tc     = WHITE if active else MUTED
            rrect(self.display, bg, rect, r=7)
            rrect(self.display, bord, rect, r=7, bw=2 if active else 1)
            s = self.fonts["small"].render(cat, True, tc)
            self.display.blit(s, (rect.x + rect.w // 2 - s.get_width() // 2,
                                  rect.y + rect.h // 2 - s.get_height() // 2))

    def draw_card_tile(self, card, pos, hovered=False):
        rx, ry = pos
        bg   = CARD_HOV if hovered else CARD_BG
        bord = CARD_BORD_ACT if hovered else CARD_BORD
        r    = pygame.Rect(rx, ry, CARD_W, CARD_H)
        rrect(self.display, bg, r, r=7)
        rrect(self.display, bord, r, r=7, bw=1)

        # Accent top stripe by category
        cat_col = CATEGORY_COLORS.get(card["category"], BLUE)
        stripe  = pygame.Rect(rx + 1, ry + 1, CARD_W - 2, 4)
        pygame.draw.rect(self.display, cat_col, stripe,
                         border_top_left_radius=6, border_top_right_radius=6)

        # Card image
        img = load_image(card["image"], CARD_W - 4, CARD_H - 24)
        self.display.blit(img, (rx + 2, ry + 6))

        # Name label at bottom
        ns = self.fonts["small"].render(card["name"], True, WHITE)
        if ns.get_width() > CARD_W - 4:
            ns = pygame.font.Font(None, 16).render(card["name"], True, WHITE)
        self.display.blit(ns, (rx + CARD_W // 2 - ns.get_width() // 2, ry + CARD_H - 16))

        # Selected highlight ring
        if self.selected_card and self.selected_card["name"] == card["name"]:
            rrect(self.display, TEAL, r, r=7, bw=2, bc=TEAL)

    def draw_grid(self):
        count = len(self.filtered)
        self.grid.update_max_scroll(count)

        # Panel behind grid
        panel_r = pygame.Rect(GRID_X - PAD, GRID_Y - 4,
                              GRID_W + PAD + 18, GRID_H + 60)
        panel(self.display, panel_r, r=10)

        # Label row
        lx, ly = GRID_X, GRID_Y - PAD + 56 + 14
        col    = CATEGORY_COLORS.get(self.active_cat, BLUE)
        self._txt(self.active_cat.upper(), lx, ly - 36, col, "small")
        self._txt(f"{count} cards", lx + 60, ly - 36, MUTED, "small")
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
        sr = pygame.Rect(sx - 8, 0, SIDEBAR_W, HEIGHT)
        panel(self.display, sr, r=0)

        # --- Sidebar content is drawn with clipping and scroll offset ---
        sidebar_clip = pygame.Rect(sx - 8, 0, SIDEBAR_W, HEIGHT)
        self.display.set_clip(sidebar_clip)

        # Calculate offset for scrolling
        oy = -self.sidebar_scroll_y

        self._txt("Card Viewer", sx + 6, 18 + oy, WHITE, "title")
        cat_col = CATEGORY_COLORS.get(self.active_cat, BLUE)
        self._txt(self.active_cat, sx + 6, 54 + oy, cat_col, "normal")
        pygame.draw.line(self.display, BORDER, (sx, 80 + oy), (WIDTH - 4, 80 + oy), 1)

        cy = 94 + oy

        # --- Card Preview Section (moved from left panel to sidebar) ---
        card = self.selected_card
        if card is not None:
            preview_w = SIDEBAR_W - 32
            cat_col_p = CATEGORY_COLORS.get(card["category"], BLUE)

            # Accent top bar
            top = pygame.Rect(sx + 6, cy, preview_w, 6)
            pygame.draw.rect(self.display, cat_col_p, top,
                             border_top_left_radius=8, border_top_right_radius=8)

            # Preview background
            prev_bg = pygame.Rect(sx + 6, cy, preview_w, 6)
            # We'll draw the image below the accent bar

            # Large image
            iw = preview_w - 8
            ih = int(iw * 1.0)
            img = load_image(card["image"], iw, ih)
            self.display.blit(img, (sx + 10, cy + 8))

            cy += ih + 14

            # Card name
            ns = self.fonts["large"].render(card["name"], True, WHITE)
            if ns.get_width() > preview_w - 8:
                ns = self.fonts["normal"].render(card["name"], True, WHITE)
            self.display.blit(ns, (sx + 6 + preview_w // 2 - ns.get_width() // 2, cy))
            cy += ns.get_height() + 4

            # Category badge
            cat_s = self.fonts["small"].render(card["category"].upper(), True, cat_col_p)
            self.display.blit(cat_s, (sx + 6 + preview_w // 2 - cat_s.get_width() // 2, cy))
            cy += cat_s.get_height() + 8

            # Description
            desc = card.get("desc", "")
            if desc:
                pygame.draw.line(self.display, BORDER,
                                 (sx + 12, cy), (sx + 6 + preview_w - 6, cy), 1)
                cy += 8
                desc_lines = wrap_text(self.fonts["desc"], desc, preview_w - 16)
                for line in desc_lines:
                    ds = self.fonts["desc"].render(line, True, MUTED)
                    self.display.blit(ds, (sx + 14, cy))
                    cy += ds.get_height() + 2
                cy += 4

            # Divider after preview
            pygame.draw.line(self.display, BORDER,
                             (sx, cy + 4), (WIDTH - 4, cy + 4), 1)
            cy += 12
        else:
            # No card selected hint
            hint_r = pygame.Rect(sx + 6, cy, SIDEBAR_W - 32, 60)
            rrect(self.display, PANEL2, hint_r, r=8)
            t = self.fonts["small"].render("Click a card to preview", True, MUTED)
            self.display.blit(t, (hint_r.centerx - t.get_width() // 2, hint_r.centery - 8))
            cy += 72

        # --- Controls ---
        controls = [
            ("ESC",   "Main menu"),
            ("D",     "Deck Manager"),
            ("R",     "Reset / All"),
            ("←/→",   "Prev/Next cat"),
            ("1–7",   "Jump to cat"),
            ("Scroll","Browse cards"),
            ("Click", "Preview card"),
        ]
        for key, desc in controls:
            kr = pygame.Rect(sx + 6, cy, 34, 20)
            rrect(self.display, (32, 44, 62), kr, r=4)
            ks = self.fonts["small"].render(key, True, BLUE)
            self.display.blit(ks, (kr.x + kr.w // 2 - ks.get_width() // 2, kr.y + 2))
            self._txt(desc, sx + 46, cy + 2, MUTED, "small")
            cy += 28

        pygame.draw.line(self.display, BORDER, (sx, cy + 2), (WIDTH - 4, cy + 2), 1)
        cy += 10

        # Category list with counts
        self._txt("Categories", sx + 6, cy, WHITE, "small"); cy += 20
        for cat in CATEGORIES[1:]:
            count = sum(1 for c in self.all_cards if c["category"] == cat)
            col   = CATEGORY_COLORS.get(cat, BLUE)
            dot   = pygame.Rect(sx + 10, cy + 4, 8, 8)
            rrect(self.display, col, dot, r=4)
            self._txt(f"{cat}", sx + 24, cy, MUTED if cat != self.active_cat else WHITE, "small")
            self._txt(f"{count}", sx + 110, cy, DIM, "small")
            cy += 20

        pygame.draw.line(self.display, BORDER, (sx, cy + 4), (WIDTH - 4, cy + 4), 1)
        cy += 12

        # Stats
        self._txt("Stats", sx + 6, cy, WHITE, "small"); cy += 20
        self._txt(f"Total cards  {len(self.all_cards)}", sx + 6, cy, MUTED, "small"); cy += 20
        self._txt(f"Showing      {len(self.filtered)}", sx + 6, cy, MUTED, "small"); cy += 20

        pygame.draw.line(self.display, BORDER, (sx, cy + 4), (WIDTH - 4, cy + 4), 1)
        cy += 12

        # Status message
        if self.status:
            col = (GREEN if any(w in self.status for w in ("Viewing","Reset","Loaded"))
                   else RED if any(w in self.status for w in ("error","No"))
                   else TEAL)
            self._txt(self.status, sx + 6, cy, col, "normal")
            cy += 28

        # Update max sidebar scroll based on content height
        content_bottom = cy + self.sidebar_scroll_y
        self._sidebar_max_scroll = max(0, content_bottom - HEIGHT + 20)

        self.display.set_clip(None)

        # Sidebar scrollbar
        if self._sidebar_max_scroll > 0:
            track = pygame.Rect(WIDTH - 6, 0, 4, HEIGHT)
            rrect(self.display, PANEL2, track, r=2)
            ratio = HEIGHT / (content_bottom)
            thumb_h = max(20, int(HEIGHT * ratio))
            frac = self.sidebar_scroll_y / max(1, self._sidebar_max_scroll)
            thumb_y = int((HEIGHT - thumb_h) * frac)
            thumb = pygame.Rect(WIDTH - 6, thumb_y, 4, thumb_h)
            rrect(self.display, TEAL, thumb, r=2)

    def draw_header(self):
        # Top bar
        bar = pygame.Rect(0, 0, WIDTH, 52)
        rrect(self.display, PANEL, bar, r=0)
        pygame.draw.line(self.display, BORDER, (0, 52), (WIDTH, 52), 1)
        self._txt("✦  Card Viewer", 20, 14, WHITE, "title")
        # Category quick-nav hint
        hint = self.fonts["small"].render("← → to switch categories  ·  click card to preview", True, DIM)
        self.display.blit(hint, (WIDTH // 2 - hint.get_width() // 2, 18))

    def draw(self):
        self.tick_status()
        self.display.fill(BG)
        self.draw_header()
        self.draw_category_tabs()
        self.draw_grid()
        self.draw_sidebar()


# =====================
# Main
# =====================
def main():
    pygame.init()
    screen  = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Card Viewer")
    clock   = pygame.time.Clock()
    viewer  = CardViewer(screen)
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