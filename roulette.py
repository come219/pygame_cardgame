# roulette.py 

import random
import math
import pygame

# =====================
# Screen
# =====================
WIDTH, HEIGHT = 1920, 1080

# =====================
# Palette (dark slate / teal accent) — from design
# =====================
BG             = (12,  14,  20 )
PANEL          = (20,  24,  34 )
PANEL2         = (26,  30,  42 )
BORDER         = (38,  46,  64 )
BORDER_HI      = (60,  80, 120 )
WHITE          = (225, 232, 245)
MUTED          = (95,  108, 132)
DIM            = (55,  65,  85 )
RED            = (210,  65,  65)
AMBER          = (215, 155,  45)
BLUE           = (75,  145, 255)
TEAL           = (45,  195, 165)
GREEN_UI       = (65,  190,  95)
PURPLE         = (145,  90, 220)
OVERLAY        = (8,   10,  16, 225)
GOLD           = (255, 215,   0)
CARD_GREY      = (18,  20,  26 )
CARD_BG        = (30,  36,  50 )

# Roulette specific colors
R_RED          = (185,  40,  40)
R_BLACK        = (28,  28,  32)
R_GREEN        = (0,  110,  50)
R_FELT         = (15,  60,  32)
R_FELT_BORDER  = (25,  90,  45)

# Chip values & colors
CHIP_VALUES = [1, 5, 10, 25, 50, 100, 500]
CHIP_COLORS = {
    1:   (220, 220, 220),
    5:   (200,  60,  60),
    10:  (60,  120, 200),
    25:  (60,  180,  80),
    50:  (200, 140,  40),
    100: (40,   40,  40),
    500: (140,  50, 180),
}

# =====================
# Roulette Variants
# =====================
# American: 0, 00, 1-36
# European: 0, 1-36
# French:   0, 1-36 (with La Partage — half back on even-money bets when 0 hits)

VARIANT_AMERICAN = "American (Double Zero)"
VARIANT_EUROPEAN = "European (Single Zero)"
VARIANT_FRENCH   = "French (La Partage)"

VARIANTS = [VARIANT_AMERICAN, VARIANT_EUROPEAN, VARIANT_FRENCH]

# Red numbers (same for all variants)
RED_NUMBERS = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}

# Wheel orders
AMERICAN_WHEEL = [
    0, 28, 9, 26, 30, 11, 7, 20, 32, 17, 5, 22, 34, 15, 3, 24, 36, 13, 1,
    "00", 27, 10, 25, 29, 12, 8, 19, 31, 18, 6, 21, 33, 16, 4, 23, 35, 14, 2
]

EUROPEAN_WHEEL = [
    0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10,
    5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26
]

# French uses same wheel as European
FRENCH_WHEEL = EUROPEAN_WHEEL


def number_color(n):
    if n == 0 or n == "00":
        return R_GREEN
    if isinstance(n, int) and n in RED_NUMBERS:
        return R_RED
    return R_BLACK


def number_str(n):
    if n == "00":
        return "00"
    return str(n)


# =====================
# Helpers
# =====================
def rrect(surf, color, rect, r=8, bw=0, bc=None):
    pygame.draw.rect(surf, color, rect, border_radius=r)
    if bw and bc:
        pygame.draw.rect(surf, bc, rect, bw, border_radius=r)


def panel_box(surf, rect, r=10):
    rrect(surf, PANEL, rect, r)
    rrect(surf, BORDER, rect, r, 1)


# =====================
# Bet types and payouts
# =====================
# Bet = (type_name, numbers_covered, payout_multiplier)
# Straight: single number, 35:1
# Split: 2 numbers, 17:1
# Street: 3 numbers, 11:1
# Corner: 4 numbers, 8:1
# Six Line: 6 numbers, 5:1
# Column: 12 numbers, 2:1
# Dozen: 12 numbers, 2:1
# Red/Black: 18 numbers, 1:1
# Odd/Even: 18 numbers, 1:1
# High/Low: 18 numbers, 1:1
# Five (American only): 0,00,1,2,3 — 6:1

EVEN_MONEY_BETS = {"Red", "Black", "Odd", "Even", "1-18", "19-36"}


def get_numbers_for_bet(bet_type, bet_data, variant):
    """Return set of winning numbers for a bet."""
    has_00 = variant == VARIANT_AMERICAN

    if bet_type == "straight":
        return {bet_data}
    elif bet_type == "red":
        return RED_NUMBERS.copy()
    elif bet_type == "black":
        return {n for n in range(1, 37) if n not in RED_NUMBERS}
    elif bet_type == "odd":
        return {n for n in range(1, 37) if n % 2 == 1}
    elif bet_type == "even":
        return {n for n in range(1, 37) if n % 2 == 0}
    elif bet_type == "low":
        return set(range(1, 19))
    elif bet_type == "high":
        return set(range(19, 37))
    elif bet_type == "dozen1":
        return set(range(1, 13))
    elif bet_type == "dozen2":
        return set(range(13, 25))
    elif bet_type == "dozen3":
        return set(range(25, 37))
    elif bet_type == "col1":
        return {n for n in range(1, 37) if n % 3 == 1}
    elif bet_type == "col2":
        return {n for n in range(1, 37) if n % 3 == 2}
    elif bet_type == "col3":
        return {n for n in range(1, 37) if n % 3 == 0}
    elif bet_type == "five" and has_00:
        return {0, "00", 1, 2, 3}
    return set()


def get_payout(bet_type):
    payouts = {
        "straight": 35, "split": 17, "street": 11, "corner": 8,
        "sixline": 5, "col1": 2, "col2": 2, "col3": 2,
        "dozen1": 2, "dozen2": 2, "dozen3": 2,
        "red": 1, "black": 1, "odd": 1, "even": 1,
        "low": 1, "high": 1, "five": 6,
    }
    return payouts.get(bet_type, 0)


def is_even_money(bet_type):
    return bet_type in ("red", "black", "odd", "even", "low", "high")


# =====================
# Game States
# =====================
ST_VARIANT_SELECT = 0
ST_BETTING        = 1
ST_SPINNING       = 2
ST_RESULT         = 3


# =====================
# Roulette Game
# =====================
class RouletteGame:
    def __init__(self, display):
        self.display = display
        self.fonts = {
            "normal":    pygame.font.Font(None, 24),
            "small":     pygame.font.Font(None, 20),
            "large":     pygame.font.Font(None, 40),
            "title":     pygame.font.Font(None, 48),
            "huge":      pygame.font.Font(None, 64),
            "chip":      pygame.font.Font(None, 16),
            "result_lg": pygame.font.Font(None, 72),
            "board":     pygame.font.Font(None, 22),
            "board_lg":  pygame.font.Font(None, 28),
            "wheel_num": pygame.font.Font(None, 18),
            "history":   pygame.font.Font(None, 20),
        }

        self.variant = VARIANT_EUROPEAN
        self.state = ST_VARIANT_SELECT

        self.balance = 1000
        self.bets = []  # list of (bet_type, bet_data, amount)
        self.selected_chip = 10

        # Wheel
        self.wheel_angle = 0.0
        self.wheel_speed = 0.0
        self.ball_angle = 0.0
        self.ball_speed = 0.0
        self.spin_phase = 0  # 0=not spinning, 1=spinning, 2=slowing, 3=stopped
        self.result_number = None
        self.result_timer = 0

        # History
        self.history = []  # last N results

        # Winnings display
        self.last_winnings = 0
        self.last_win_bets = []

        # Board layout
        self.board_rects = {}  # key -> pygame.Rect
        self.hover_bet = None

        self.status = ""
        self.status_timer = 0

    def set_status(self, msg, dur=100):
        self.status = msg
        self.status_timer = dur

    def tick_status(self):
        if self.status_timer > 0:
            self.status_timer -= 1
            if self.status_timer == 0:
                self.status = ""

    def txt(self, text, x, y, color=WHITE, fk="normal", center=False):
        s = self.fonts[fk].render(str(text), True, color)
        if center:
            self.display.blit(s, (x - s.get_width() // 2, y - s.get_height() // 2))
        else:
            self.display.blit(s, (x, y))

    def get_wheel(self):
        if self.variant == VARIANT_AMERICAN:
            return AMERICAN_WHEEL
        return EUROPEAN_WHEEL  # European and French use same wheel

    def has_00(self):
        return self.variant == VARIANT_AMERICAN

    def all_numbers(self):
        nums = list(range(0, 37))
        if self.has_00():
            nums.append("00")
        return nums

    def total_bet(self):
        return sum(a for _, _, a in self.bets)

    # ===================================================================
    # VARIANT SELECT
    # ===================================================================
    def draw_variant_select(self):
        self.display.fill(BG)
        self.txt("ROULETTE", WIDTH // 2, 80, GOLD, "huge", center=True)
        self.txt("Choose your variant", WIDTH // 2, 140, MUTED, "normal", center=True)

        mx, my = pygame.mouse.get_pos()
        descs = [
            ("American (Double Zero)", "0 and 00  •  House edge 5.26%", "38 numbers  •  Standard US casino rules"),
            ("European (Single Zero)", "0 only  •  House edge 2.70%", "37 numbers  •  Standard UK/EU casino rules"),
            ("French (La Partage)", "0 only  •  House edge 1.35% on even bets", "37 numbers  •  Half back on even-money bets when 0 hits"),
        ]

        card_w, card_h = 480, 280
        gap = 40
        total_w = len(descs) * card_w + (len(descs) - 1) * gap
        sx = (WIDTH - total_w) // 2
        sy = (HEIGHT - card_h) // 2 - 20

        for i, (title, sub, desc) in enumerate(descs):
            r = pygame.Rect(sx + i * (card_w + gap), sy, card_w, card_h)
            hov = r.collidepoint(mx, my)
            selected = VARIANTS[i] == self.variant

            if selected:
                bg = (25, 55, 40)
                bord = GREEN_UI
            elif hov:
                bg = (28, 36, 52)
                bord = BLUE
            else:
                bg = PANEL
                bord = BORDER

            rrect(self.display, bg, r, r=14)
            rrect(self.display, bord, r, r=14, bw=2 if (hov or selected) else 1)

            # Variant badge
            badge_colors = [R_RED, R_GREEN, PURPLE]
            badge_r = pygame.Rect(r.x + 15, r.y + 15, 90, 28)
            rrect(self.display, badge_colors[i], badge_r, r=6)
            badge_labels = ["US", "UK/EU", "FR"]
            self.txt(badge_labels[i], badge_r.centerx, badge_r.centery, WHITE, "normal", center=True)

            self.txt(title, r.centerx, r.y + 70, WHITE, "normal", center=True)
            self.txt(sub, r.centerx, r.y + 100, TEAL, "small", center=True)

            # Divider
            pygame.draw.line(self.display, BORDER, (r.x + 20, r.y + 125), (r.right - 20, r.y + 125), 1)

            self.txt(desc, r.centerx, r.y + 150, MUTED, "small", center=True)

            # Mini wheel preview
            wheel = AMERICAN_WHEEL if i == 0 else EUROPEAN_WHEEL
            wcx, wcy = r.centerx, r.y + 210
            wrad = 40
            pygame.draw.circle(self.display, (30, 40, 30), (wcx, wcy), wrad)
            pygame.draw.circle(self.display, R_FELT_BORDER, (wcx, wcy), wrad, 2)
            n_nums = len(wheel)
            for j, num in enumerate(wheel):
                angle = 2 * math.pi * j / n_nums - math.pi / 2
                nx = wcx + int((wrad - 8) * math.cos(angle))
                ny = wcy + int((wrad - 8) * math.sin(angle))
                col = number_color(num)
                pygame.draw.circle(self.display, col, (nx, ny), 3)

            if selected:
                self.txt("✓ SELECTED", r.centerx, r.bottom - 25, GREEN_UI, "small", center=True)
            else:
                self.txt("Click to select", r.centerx, r.bottom - 25, DIM, "small", center=True)

        # Play button
        play_r = pygame.Rect(WIDTH // 2 - 120, sy + card_h + 40, 240, 52)
        hov_play = play_r.collidepoint(mx, my)
        bg = GREEN_UI if not hov_play else (95, 220, 125)
        rrect(self.display, bg, play_r, r=10)
        rrect(self.display, (100, 220, 130), play_r, r=10, bw=2 if hov_play else 1)
        self.txt("PLAY ROULETTE", play_r.centerx, play_r.centery, WHITE, "large", center=True)

        self.txt("ESC to quit  •  Click variant then PLAY or press ENTER", WIDTH // 2, HEIGHT - 30, DIM, "small", center=True)

    # ===================================================================
    # BOARD LAYOUT
    # ===================================================================
    def build_board_rects(self):
        """Build clickable rectangles for the betting board."""
        self.board_rects = {}

        # Board position
        bx = 80
        by = 160
        cw = 46   # cell width
        ch = 50   # cell height

        has_00 = self.has_00()

        # Zero(s) — tall cells on the left
        if has_00:
            # 0 on top, 00 on bottom
            self.board_rects[("straight", 0)] = pygame.Rect(bx, by, cw, ch * 1.5)
            self.board_rects[("straight", "00")] = pygame.Rect(bx, by + int(ch * 1.5), cw, ch * 1.5)
        else:
            # Single 0 spanning full height
            self.board_rects[("straight", 0)] = pygame.Rect(bx, by, cw, ch * 3)

        # Number grid: 3 rows x 12 columns
        # Row 1 (top): 3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36
        # Row 2 (mid): 2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35
        # Row 3 (bot): 1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34
        grid_x = bx + cw + 2
        for col in range(12):
            for row in range(3):
                num = (col * 3) + (3 - row)
                rx = grid_x + col * cw
                ry = by + row * ch
                self.board_rects[("straight", num)] = pygame.Rect(rx, ry, cw, ch)

        # Bottom area for outside bets
        bot_y = by + 3 * ch + 4

        # Columns (2:1)
        col_x = grid_x + 12 * cw + 2
        for row in range(3):
            label = f"col{3 - row}"
            self.board_rects[(label, None)] = pygame.Rect(col_x, by + row * ch, cw + 10, ch)

        # Dozens
        dozen_w = 4 * cw
        for d in range(3):
            label = f"dozen{d + 1}"
            self.board_rects[(label, None)] = pygame.Rect(grid_x + d * dozen_w, bot_y, dozen_w, ch * 0.7)

        # Even-money bets
        em_y = bot_y + int(ch * 0.7) + 4
        em_w = 2 * cw
        em_labels = [("low", "1-18"), ("even", "EVEN"), ("red", "RED"),
                     ("black", "BLACK"), ("odd", "ODD"), ("high", "19-36")]
        for ei, (bt, lbl) in enumerate(em_labels):
            self.board_rects[(bt, lbl)] = pygame.Rect(grid_x + ei * em_w, em_y, em_w, ch * 0.7)

        # Five bet (American only)
        if has_00:
            five_y = by + 3 * ch + 4 + int(ch * 0.7) + 4 + int(ch * 0.7) + 4
            self.board_rects[("five", None)] = pygame.Rect(bx, five_y, cw * 3, int(ch * 0.6))

    def draw_board(self):
        """Draw the betting board."""
        if not self.board_rects:
            self.build_board_rects()

        mx, my = pygame.mouse.get_pos()
        self.hover_bet = None

        for (bt, bd), rect in self.board_rects.items():
            hov = rect.collidepoint(mx, my) and self.state == ST_BETTING
            if hov:
                self.hover_bet = (bt, bd)

            # Determine color
            if bt == "straight":
                col = number_color(bd)
                if col == R_GREEN:
                    bg = R_GREEN
                elif col == R_RED:
                    bg = R_RED if not hov else (210, 60, 60)
                else:
                    bg = R_BLACK if not hov else (50, 50, 58)
            elif bt == "red":
                bg = R_RED if not hov else (210, 60, 60)
            elif bt == "black":
                bg = R_BLACK if not hov else (50, 50, 58)
            elif bt in ("col1", "col2", "col3", "dozen1", "dozen2", "dozen3"):
                bg = R_FELT if not hov else (25, 80, 45)
            elif bt == "five":
                bg = R_GREEN if not hov else (10, 130, 60)
            else:
                bg = R_FELT if not hov else (25, 80, 45)

            rrect(self.display, bg, rect, r=4)
            bord_col = GOLD if hov else (60, 80, 60)
            rrect(self.display, bord_col, rect, r=4, bw=2 if hov else 1)

            # Label
            if bt == "straight":
                label = number_str(bd)
                tc = WHITE
            elif bt == "red":
                label = "RED"
                tc = WHITE
            elif bt == "black":
                label = "BLACK"
                tc = WHITE
            elif bt == "low":
                label = "1-18"
                tc = WHITE
            elif bt == "high":
                label = "19-36"
                tc = WHITE
            elif bt == "even":
                label = "EVEN"
                tc = WHITE
            elif bt == "odd":
                label = "ODD"
                tc = WHITE
            elif bt == "col1":
                label = "2:1"
                tc = WHITE
            elif bt == "col2":
                label = "2:1"
                tc = WHITE
            elif bt == "col3":
                label = "2:1"
                tc = WHITE
            elif bt == "dozen1":
                label = "1st 12"
                tc = WHITE
            elif bt == "dozen2":
                label = "2nd 12"
                tc = WHITE
            elif bt == "dozen3":
                label = "3rd 12"
                tc = WHITE
            elif bt == "five":
                label = "0-00-1-2-3"
                tc = WHITE
            else:
                label = str(bd) if bd else bt
                tc = WHITE

            fk = "board" if len(label) <= 3 else "small"
            self.txt(label, rect.centerx, rect.centery, tc, fk, center=True)

            # Show bet amount on this spot
            bet_on = sum(a for btype, bdata, a in self.bets if btype == bt and bdata == bd)
            if bet_on > 0:
                # Draw chip on cell
                chip_r = min(14, rect.width // 3)
                cx_c = rect.right - chip_r - 2
                cy_c = rect.y + chip_r + 2
                pygame.draw.circle(self.display, GOLD, (cx_c, cy_c), chip_r)
                pygame.draw.circle(self.display, WHITE, (cx_c, cy_c), chip_r, 1)
                t = self.fonts["chip"].render(str(bet_on), True, (20, 20, 20))
                self.display.blit(t, (cx_c - t.get_width() // 2, cy_c - t.get_height() // 2))

        # Highlight winning number on board
        if self.state in (ST_RESULT,) and self.result_number is not None:
            key = ("straight", self.result_number)
            if key in self.board_rects:
                wr = self.board_rects[key]
                rrect(self.display, GOLD, wr.inflate(6, 6), r=6, bw=3)

    # ===================================================================
    # WHEEL DRAWING
    # ===================================================================
    def draw_wheel(self, cx, cy, radius):
        wheel = self.get_wheel()
        n = len(wheel)
        angle_per = 2 * math.pi / n

        # Outer ring
        pygame.draw.circle(self.display, (50, 40, 30), (cx, cy), radius + 8)
        pygame.draw.circle(self.display, (80, 65, 45), (cx, cy), radius + 8, 3)
        pygame.draw.circle(self.display, (40, 30, 20), (cx, cy), radius)

        # Number segments
        for i, num in enumerate(wheel):
            a_start = self.wheel_angle + i * angle_per - angle_per / 2
            a_end = a_start + angle_per
            col = number_color(num)

            # Draw segment as polygon
            pts = [(cx, cy)]
            steps = 8
            for s in range(steps + 1):
                a = a_start + (a_end - a_start) * s / steps
                pts.append((cx + int(radius * math.cos(a)),
                            cy + int(radius * math.sin(a))))
            if len(pts) >= 3:
                pygame.draw.polygon(self.display, col, pts)
                pygame.draw.polygon(self.display, (20, 20, 20), pts, 1)

            # Number text
            a_mid = a_start + angle_per / 2
            tr = radius * 0.78
            tx = cx + int(tr * math.cos(a_mid))
            ty = cy + int(tr * math.sin(a_mid))
            ns = self.fonts["wheel_num"].render(number_str(num), True, WHITE)
            # Rotate text (approximate by just placing it)
            self.display.blit(ns, (tx - ns.get_width() // 2, ty - ns.get_height() // 2))

        # Inner circle
        pygame.draw.circle(self.display, (35, 30, 25), (cx, cy), int(radius * 0.5))
        pygame.draw.circle(self.display, (60, 50, 35), (cx, cy), int(radius * 0.5), 2)
        pygame.draw.circle(self.display, (25, 20, 15), (cx, cy), int(radius * 0.35))

        # Ball
        if self.spin_phase > 0:
            ball_r = radius * 0.88
            bx = cx + int(ball_r * math.cos(self.ball_angle))
            by = cy + int(ball_r * math.sin(self.ball_angle))
            pygame.draw.circle(self.display, (240, 240, 240), (bx, by), 8)
            pygame.draw.circle(self.display, (200, 200, 200), (bx, by), 8, 2)
            # Shine
            pygame.draw.circle(self.display, WHITE, (bx - 2, by - 2), 3)

        # Pointer (top)
        ptr_pts = [(cx, cy - radius - 12), (cx - 8, cy - radius - 24), (cx + 8, cy - radius - 24)]
        pygame.draw.polygon(self.display, GOLD, ptr_pts)
        pygame.draw.polygon(self.display, (200, 170, 0), ptr_pts, 2)

    # ===================================================================
    # CHIP SELECTOR
    # ===================================================================
    def draw_chip_selector(self):
        mx, my = pygame.mouse.get_pos()
        sx = WIDTH - 350
        sy = HEIGHT - 80
        self.txt("SELECT CHIP", sx, sy - 22, MUTED, "small")

        for i, cv in enumerate(CHIP_VALUES):
            ccx = sx + i * 44 + 20
            ccy = sy + 20
            selected = cv == self.selected_chip
            dist = ((mx - ccx)**2 + (my - ccy)**2) ** 0.5
            hov = dist < 20

            rad = 22 if selected else (19 if hov else 16)
            col = CHIP_COLORS.get(cv, BLUE)

            if selected:
                pygame.draw.circle(self.display, GOLD, (ccx, ccy), rad + 3, 2)

            pygame.draw.circle(self.display, col, (ccx, ccy), rad)
            pygame.draw.circle(self.display, WHITE, (ccx, ccy), rad, 2)
            pygame.draw.circle(self.display, col, (ccx, ccy), rad - 3)

            for a in range(0, 360, 45):
                r1 = rad - 5
                r2 = rad - 1
                x1 = ccx + int(r1 * math.cos(math.radians(a)))
                y1 = ccy + int(r1 * math.sin(math.radians(a)))
                x2 = ccx + int(r2 * math.cos(math.radians(a)))
                y2 = ccy + int(r2 * math.sin(math.radians(a)))
                pygame.draw.line(self.display, WHITE, (x1, y1), (x2, y2), 2)

            t = self.fonts["chip"].render(str(cv), True, WHITE)
            self.display.blit(t, (ccx - t.get_width() // 2, ccy - t.get_height() // 2))

    def chip_selector_click(self, pos):
        sx = WIDTH - 350
        sy = HEIGHT - 80
        mx, my = pos
        for i, cv in enumerate(CHIP_VALUES):
            ccx = sx + i * 44 + 20
            ccy = sy + 20
            dist = ((mx - ccx)**2 + (my - ccy)**2) ** 0.5
            if dist < 22:
                self.selected_chip = cv
                return True
        return False

    # ===================================================================
    # HISTORY
    # ===================================================================
    def draw_history(self):
        hx = WIDTH - 350
        hy = 160
        panel_box(self.display, pygame.Rect(hx - 10, hy - 30, 360, 260), r=10)
        self.txt("HISTORY", hx, hy - 22, MUTED, "small")

        # Show last 50 results in a grid
        cols = 10
        for i, num in enumerate(reversed(self.history[-50:])):
            col_i = i % cols
            row_i = i // cols
            nx = hx + col_i * 34
            ny = hy + 8 + row_i * 34
            nc = number_color(num)
            pygame.draw.circle(self.display, nc, (nx + 14, ny + 14), 14)
            pygame.draw.circle(self.display, (80, 80, 80), (nx + 14, ny + 14), 14, 1)
            ns = self.fonts["history"].render(number_str(num), True, WHITE)
            self.display.blit(ns, (nx + 14 - ns.get_width() // 2, ny + 14 - ns.get_height() // 2))

        if not self.history:
            self.txt("No spins yet", hx + 80, hy + 60, DIM, "small")

    # ===================================================================
    # BETTING SCREEN
    # ===================================================================
    def draw_betting_screen(self):
        self.display.fill(BG)

        # Title bar
        self.txt("ROULETTE", 20, 15, GOLD, "title")
        variant_short = {"American (Double Zero)": "US Double-Zero",
                         "European (Single Zero)": "EU Single-Zero",
                         "French (La Partage)": "FR La Partage"}.get(self.variant, self.variant)
        self.txt(variant_short, 260, 25, TEAL, "normal")

        # Balance
        self.txt(f"Balance: ${self.balance}", 20, 55, WHITE, "normal")
        total = self.total_bet()
        if total > 0:
            self.txt(f"Total Bet: ${total}", 200, 55, GOLD, "normal")

        # Board
        self.draw_board()

        # Wheel (right side)
        wcx = WIDTH - 540
        wcy = 560
        wrad = 180
        self.draw_wheel(wcx, wcy, wrad)

        # History
        self.draw_history()

        # Chip selector
        self.draw_chip_selector()

        # Action buttons
        mx, my = pygame.mouse.get_pos()

        # Spin button
        can_spin = total > 0
        spin_r = pygame.Rect(WIDTH - 700, HEIGHT - 80, 160, 50)
        hov = spin_r.collidepoint(mx, my) and can_spin
        bg = GREEN_UI if can_spin else CARD_GREY
        if hov:
            bg = (95, 220, 125)
        rrect(self.display, bg, spin_r, r=10)
        rrect(self.display, (100, 220, 130) if can_spin else BORDER, spin_r, r=10, bw=2 if hov else 1)
        self.txt("SPIN", spin_r.centerx, spin_r.centery, WHITE if can_spin else DIM, "large", center=True)

        # Clear bets
        clear_r = pygame.Rect(WIDTH - 700, HEIGHT - 25, 100, 30)
        hov_c = clear_r.collidepoint(mx, my) and total > 0
        rrect(self.display, RED if hov_c else (80, 30, 30), clear_r, r=6)
        self.txt("Clear All", clear_r.centerx, clear_r.centery, WHITE, "small", center=True)

        # Undo last bet
        undo_r = pygame.Rect(WIDTH - 590, HEIGHT - 25, 80, 30)
        hov_u = undo_r.collidepoint(mx, my) and len(self.bets) > 0
        rrect(self.display, AMBER if hov_u else (80, 60, 20), undo_r, r=6)
        self.txt("Undo", undo_r.centerx, undo_r.centery, WHITE, "small", center=True)

        # Back to variant select
        back_r = pygame.Rect(WIDTH - 160, 15, 140, 34)
        hov_b = back_r.collidepoint(mx, my)
        rrect(self.display, PANEL2 if not hov_b else (40, 50, 70), back_r, r=8)
        rrect(self.display, BORDER, back_r, r=8, bw=1)
        self.txt("← Variants", back_r.centerx, back_r.centery, MUTED, "normal", center=True)

        # Hover info
        if self.hover_bet and self.state == ST_BETTING:
            bt, bd = self.hover_bet
            payout = get_payout(bt)
            info = f"Pays {payout}:1"
            if bt == "straight":
                info = f"{number_str(bd)} — Straight Up — Pays 35:1"
            elif bt in ("red", "black", "odd", "even", "low", "high"):
                info = f"{bt.upper()} — Even Money — Pays 1:1"
            elif bt.startswith("dozen"):
                info = f"Dozen — Pays 2:1"
            elif bt.startswith("col"):
                info = f"Column — Pays 2:1"
            elif bt == "five":
                info = f"Five Number — Pays 6:1"
            self.txt(info, 80, HEIGHT - 25, MUTED, "small")

        # Keyboard hints
        self.txt("ENTER=Spin  C=Clear  Z=Undo  1-7=Chip  ESC=Back", WIDTH // 2, 100, DIM, "small", center=True)

    # ===================================================================
    # SPINNING / RESULT SCREEN
    # ===================================================================
    def draw_spin_screen(self):
        self.display.fill(BG)

        self.txt("ROULETTE", 20, 15, GOLD, "title")
        self.txt(f"Balance: ${self.balance}", 20, 55, WHITE, "normal")

        # Board (dimmed during spin)
        self.draw_board()

        # Big wheel in center
        wcx = WIDTH - 540
        wcy = 500
        wrad = 220
        self.draw_wheel(wcx, wcy, wrad)

        # History
        self.draw_history()

        if self.state == ST_SPINNING:
            self.txt("SPINNING...", wcx, wcy - wrad - 50, GOLD, "large", center=True)
        elif self.state == ST_RESULT:
            # Result display
            num = self.result_number
            col = number_color(num)
            ns = number_str(num)

            # Big result
            result_r = pygame.Rect(wcx - 80, wcy - wrad - 100, 160, 80)
            rrect(self.display, col, result_r, r=12)
            rrect(self.display, GOLD, result_r, r=12, bw=3)
            self.txt(ns, result_r.centerx, result_r.centery - 5, WHITE, "result_lg", center=True)

            col_name = "GREEN" if col == R_GREEN else ("RED" if col == R_RED else "BLACK")
            self.txt(col_name, result_r.centerx, result_r.bottom + 10, col, "normal", center=True)

            # Winnings
            if self.last_winnings > 0:
                self.txt(f"WON ${self.last_winnings}!", wcx, result_r.bottom + 40, GOLD, "large", center=True)
            elif self.total_bet() == 0 and self.last_winnings == 0:
                self.txt("No wins this round", wcx, result_r.bottom + 40, MUTED, "normal", center=True)

            # Continue button
            mx, my = pygame.mouse.get_pos()
            cont_r = pygame.Rect(wcx - 100, HEIGHT - 80, 200, 50)
            hov = cont_r.collidepoint(mx, my)
            bg = GREEN_UI if not hov else (95, 220, 125)
            rrect(self.display, bg, cont_r, r=10)
            rrect(self.display, (100, 220, 130), cont_r, r=10, bw=2 if hov else 1)
            self.txt("NEW ROUND", cont_r.centerx, cont_r.centery, WHITE, "normal", center=True)

            self.txt("ENTER for new round  •  ESC for variants", WIDTH // 2, HEIGHT - 20, DIM, "small", center=True)

    # ===================================================================
    # SPIN LOGIC
    # ===================================================================
    def start_spin(self):
        if self.total_bet() <= 0:
            self.set_status("Place a bet first!")
            return
        self.state = ST_SPINNING
        self.spin_phase = 1
        self.wheel_speed = random.uniform(0.02, 0.04)
        self.ball_speed = -random.uniform(0.08, 0.14)
        self.result_number = None
        self.result_timer = 0

        # Pre-determine result
        wheel = self.get_wheel()
        self.result_number = random.choice(wheel)

    def update_spin(self):
        if self.spin_phase == 0:
            return

        # Spin wheel
        self.wheel_angle += self.wheel_speed

        # Ball
        self.ball_angle += self.ball_speed

        # Slow down
        if self.spin_phase == 1:
            self.ball_speed *= 0.993
            self.wheel_speed *= 0.998
            if abs(self.ball_speed) < 0.01:
                self.spin_phase = 2
                self.result_timer = 0

        if self.spin_phase == 2:
            # Settle ball to result position
            wheel = self.get_wheel()
            n = len(wheel)
            target_idx = wheel.index(self.result_number)
            target_angle = self.wheel_angle + (2 * math.pi * target_idx / n) - math.pi / 2
            # Lerp ball to target
            diff = target_angle - self.ball_angle
            while diff > math.pi:
                diff -= 2 * math.pi
            while diff < -math.pi:
                diff += 2 * math.pi
            self.ball_angle += diff * 0.08
            self.wheel_speed *= 0.98

            self.result_timer += 1
            if self.result_timer > 60:
                self.spin_phase = 3
                self._resolve_bets()

        if self.spin_phase == 3:
            self.wheel_speed *= 0.95
            if abs(self.wheel_speed) < 0.0001:
                self.wheel_speed = 0

    def _resolve_bets(self):
        self.state = ST_RESULT
        num = self.result_number
        self.history.append(num)

        total_won = 0
        self.last_win_bets = []

        for bt, bd, amt in self.bets:
            winning_nums = get_numbers_for_bet(bt, bd, self.variant)
            if num in winning_nums:
                payout = get_payout(bt)
                winnings = amt * payout + amt  # payout + original bet
                total_won += winnings
                self.last_win_bets.append((bt, bd, amt, winnings))
            elif self.variant == VARIANT_FRENCH and is_even_money(bt) and num == 0:
                # La Partage: return half on even-money bets when 0
                refund = amt // 2
                total_won += refund
                self.last_win_bets.append((bt, bd, amt, refund))

        self.balance += total_won
        self.last_winnings = total_won - self.total_bet() if total_won > 0 else 0
        if self.last_winnings < 0:
            self.last_winnings = 0

        # Actually compute net: total_won is what comes back
        # We already deducted bets when placing them, and total_won includes original bet for winners
        # So last_winnings for display = total_won (since bets were already deducted)
        self.last_winnings = total_won

    def new_round(self):
        self.bets = []
        self.spin_phase = 0
        self.result_number = None
        self.hover_bet = None
        if self.balance <= 0:
            self.balance = 1000
            self.set_status("Out of chips! Balance reset to $1000")
        self.state = ST_BETTING

    # ===================================================================
    # EVENTS
    # ===================================================================
    def handle_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return False

            if self.state == ST_VARIANT_SELECT:
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    self._ev_variant_click(e.pos)
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        return False
                    elif e.key == pygame.K_RETURN:
                        self.state = ST_BETTING
                        self.build_board_rects()

            elif self.state == ST_BETTING:
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    self._ev_bet_click(e.pos)
                elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 3:
                    # Right-click to remove bet
                    self._ev_bet_rclick(e.pos)
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        # Return bets
                        self.balance += self.total_bet()
                        self.bets = []
                        self.state = ST_VARIANT_SELECT
                    elif e.key == pygame.K_RETURN:
                        self.start_spin()
                    elif e.key == pygame.K_c:
                        self.balance += self.total_bet()
                        self.bets = []
                    elif e.key == pygame.K_z:
                        if self.bets:
                            _, _, amt = self.bets.pop()
                            self.balance += amt
                    elif e.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4,
                                   pygame.K_5, pygame.K_6, pygame.K_7):
                        idx = e.key - pygame.K_1
                        if 0 <= idx < len(CHIP_VALUES):
                            self.selected_chip = CHIP_VALUES[idx]

            elif self.state == ST_SPINNING:
                pass  # No input during spin

            elif self.state == ST_RESULT:
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    mx, my = e.pos
                    wcx = WIDTH - 540
                    cont_r = pygame.Rect(wcx - 100, HEIGHT - 80, 200, 50)
                    if cont_r.collidepoint(e.pos):
                        self.new_round()
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_RETURN:
                        self.new_round()
                    elif e.key == pygame.K_ESCAPE:
                        self.bets = []
                        self.spin_phase = 0
                        self.state = ST_VARIANT_SELECT

        return True

    def _ev_variant_click(self, pos):
        mx, my = pos
        card_w, card_h = 480, 280
        gap = 40
        total_w = 3 * card_w + 2 * gap
        sx = (WIDTH - total_w) // 2
        sy = (HEIGHT - card_h) // 2 - 20

        for i in range(3):
            r = pygame.Rect(sx + i * (card_w + gap), sy, card_w, card_h)
            if r.collidepoint(pos):
                self.variant = VARIANTS[i]
                self.build_board_rects()
                return

        play_r = pygame.Rect(WIDTH // 2 - 120, sy + card_h + 40, 240, 52)
        if play_r.collidepoint(pos):
            self.state = ST_BETTING
            self.build_board_rects()

    def _ev_bet_click(self, pos):
        # Chip selector
        if self.chip_selector_click(pos):
            return

        # Spin button
        spin_r = pygame.Rect(WIDTH - 700, HEIGHT - 80, 160, 50)
        if spin_r.collidepoint(pos) and self.total_bet() > 0:
            self.start_spin()
            return

        # Clear
        clear_r = pygame.Rect(WIDTH - 700, HEIGHT - 25, 100, 30)
        if clear_r.collidepoint(pos):
            self.balance += self.total_bet()
            self.bets = []
            return

        # Undo
        undo_r = pygame.Rect(WIDTH - 590, HEIGHT - 25, 80, 30)
        if undo_r.collidepoint(pos) and self.bets:
            _, _, amt = self.bets.pop()
            self.balance += amt
            return

        # Back
        back_r = pygame.Rect(WIDTH - 160, 15, 140, 34)
        if back_r.collidepoint(pos):
            self.balance += self.total_bet()
            self.bets = []
            self.state = ST_VARIANT_SELECT
            return

        # Board bets
        if self.hover_bet:
            bt, bd = self.hover_bet
            amt = self.selected_chip
            if self.balance >= amt:
                self.bets.append((bt, bd, amt))
                self.balance -= amt
            else:
                self.set_status("Not enough balance!")

    def _ev_bet_rclick(self, pos):
        """Right-click to remove last bet on hovered spot."""
        if self.hover_bet:
            bt, bd = self.hover_bet
            # Find last bet matching this spot
            for i in range(len(self.bets) - 1, -1, -1):
                if self.bets[i][0] == bt and self.bets[i][1] == bd:
                    _, _, amt = self.bets.pop(i)
                    self.balance += amt
                    return

    # ===================================================================
    # UPDATE & DRAW
    # ===================================================================
    def update(self):
        self.tick_status()
        if self.state == ST_SPINNING:
            self.update_spin()

    def draw(self):
        self.update()

        if self.state == ST_VARIANT_SELECT:
            self.draw_variant_select()
        elif self.state == ST_BETTING:
            self.draw_betting_screen()
        elif self.state in (ST_SPINNING, ST_RESULT):
            self.draw_spin_screen()

        # Status
        if self.status:
            sr = pygame.Rect(WIDTH // 2 - 200, HEIGHT - 55, 400, 30)
            rrect(self.display, PANEL, sr, r=8)
            rrect(self.display, BORDER, sr, r=8, bw=1)
            col = GREEN_UI if "Won" in self.status or "reset" in self.status else \
                  RED if "Not" in self.status or "Out" in self.status else WHITE
            self.txt(self.status, sr.centerx, sr.centery, col, "small", center=True)


# =====================
# Main
# =====================
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Roulette")
    clock = pygame.time.Clock()
    game = RouletteGame(screen)

    running = True
    while running:
        running = game.handle_events()
        game.draw()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()