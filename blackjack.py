# blackjack.py


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
GOLD           = (255, 215,   0)
DARK_GREEN     = (15,  55,  30)
FELT_GREEN     = (20,  75,  40)
FELT_BORDER    = (30, 100,  50)

# Card dimensions
CARD_W, CARD_H = 90, 130
CARD_OVERLAP   = 30

# Seat layout
MAX_SEATS      = 5
SEAT_W         = 310
SEAT_H         = 320

# Chip values
CHIP_VALUES = [5, 10, 25, 50, 100, 500]
CHIP_COLORS = {
    5:   (200,  60,  60),
    10:  (60,  120, 200),
    25:  (60,  180,  80),
    50:  (200, 140,  40),
    100: (40,   40,  40),
    500: (140,  50, 180),
}

# Suits & Ranks
SUITS  = ["Hearts", "Diamonds", "Clubs", "Spades"]
RANKS  = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
SUIT_SYM    = {"Hearts": "♥", "Diamonds": "♦", "Clubs": "♣", "Spades": "♠"}
SUIT_COLORS = {"Hearts": RED, "Diamonds": RED, "Clubs": WHITE, "Spades": WHITE}

# Game states
ST_SEAT_SELECT = 0
ST_BETTING     = 1
ST_DEALING     = 2
ST_PLAYER      = 3
ST_DEALER      = 4
ST_RESOLVE     = 5
ST_ROUND_OVER  = 6


# =====================
# Helpers (from design)
# =====================
def rrect(surf, color, rect, r=8, bw=0, bc=None):
    pygame.draw.rect(surf, color, rect, border_radius=r)
    if bw and bc:
        pygame.draw.rect(surf, bc, rect, bw, border_radius=r)


def panel_box(surf, rect, r=10):
    rrect(surf, PANEL, rect, r)
    rrect(surf, BORDER, rect, r, 1)


def clamp(val, lo, hi):
    return max(lo, min(hi, val))


# =====================
# Card
# =====================
class Card:
    __slots__ = ("rank", "suit", "face_up")

    def __init__(self, rank, suit, face_up=True):
        self.rank = rank
        self.suit = suit
        self.face_up = face_up

    def bj_value(self):
        if self.rank in ("J", "Q", "K"):
            return 10
        if self.rank == "A":
            return 11
        return int(self.rank)

    def __repr__(self):
        return f"{self.rank}{SUIT_SYM.get(self.suit, '?')}"


# =====================
# Shoe
# =====================
class Shoe:
    def __init__(self, num_decks=6):
        self.num_decks = num_decks
        self.cards = []
        self.reshuffle()

    def reshuffle(self):
        self.cards = [Card(r, s) for _ in range(self.num_decks) for s in SUITS for r in RANKS]
        random.shuffle(self.cards)

    def deal(self, face_up=True):
        if len(self.cards) < 20:
            self.reshuffle()
        c = self.cards.pop()
        c.face_up = face_up
        return c

    def remaining(self):
        return len(self.cards)


# =====================
# Hand helpers
# =====================
def hand_value(cards, only_visible=True):
    """Returns (total, is_soft)."""
    total = 0
    aces = 0
    for c in cards:
        if only_visible and not c.face_up:
            continue
        if c.rank == "A":
            aces += 1
            total += 11
        elif c.rank in ("J", "Q", "K"):
            total += 10
        else:
            total += int(c.rank)
    soft = aces > 0
    while total > 21 and aces > 0:
        total -= 10
        aces -= 1
    if aces == 0:
        soft = False
    return total, soft


def hand_total(cards):
    v, _ = hand_value(cards, only_visible=False)
    return v


def is_blackjack(cards):
    return len(cards) == 2 and hand_total(cards) == 21


# =====================
# Hand / Seat
# =====================
class Hand:
    def __init__(self):
        self.cards = []
        self.bet = 0
        self.stood = False
        self.doubled = False
        self.surrendered = False
        self.result = None   # "win","lose","push","blackjack","surrender"
        self.payout = 0

    def add(self, card):
        self.cards.append(card)

    def val(self):
        return hand_value(self.cards, only_visible=False)

    def total(self):
        return hand_total(self.cards)

    def busted(self):
        return self.total() > 21

    def is_bj(self):
        return is_blackjack(self.cards)

    def can_split(self):
        if len(self.cards) != 2:
            return False
        return self.cards[0].bj_value() == self.cards[1].bj_value()

    def can_double(self):
        return len(self.cards) == 2 and not self.doubled

    def done(self):
        return self.stood or self.busted() or self.surrendered or self.is_bj()


class Seat:
    def __init__(self, idx):
        self.idx = idx
        self.occupied = False
        self.balance = 1000
        self.hands = []
        self.hand_idx = 0
        self.name = f"Seat {idx + 1}"

    def reset(self):
        self.hands = []
        self.hand_idx = 0

    def cur_hand(self):
        if 0 <= self.hand_idx < len(self.hands):
            return self.hands[self.hand_idx]
        return None

    def all_done(self):
        return all(h.done() for h in self.hands)

    def advance(self):
        self.hand_idx += 1
        return self.hand_idx < len(self.hands)


# =====================
# Button
# =====================
class Btn:
    def __init__(self, rect, label, color=BLUE, enabled=True):
        self.rect = pygame.Rect(rect)
        self.label = label
        self.color = color
        self.enabled = enabled

    def draw(self, surf, fonts):
        mx, my = pygame.mouse.get_pos()
        hov = self.rect.collidepoint(mx, my) and self.enabled
        if not self.enabled:
            bg, bord, tc = CARD_GREY, BORDER, DIM
        elif hov:
            bg = tuple(min(255, c + 35) for c in self.color)
            bord, tc = WHITE, WHITE
        else:
            bg = self.color
            bord = tuple(min(255, c + 20) for c in self.color)
            tc = WHITE
        rrect(surf, bg, self.rect, r=8)
        rrect(surf, bord, self.rect, r=8, bw=2 if hov else 1)
        s = fonts["normal"].render(self.label, True, tc)
        surf.blit(s, (self.rect.centerx - s.get_width() // 2,
                       self.rect.centery - s.get_height() // 2))

    def hit(self, pos):
        return self.enabled and self.rect.collidepoint(pos)


# =====================
# Blackjack Game
# =====================
class BlackjackGame:
    def __init__(self, display):
        self.display = display
        self.fonts = {
            "normal":    pygame.font.Font(None, 24),
            "small":     pygame.font.Font(None, 20),
            "large":     pygame.font.Font(None, 40),
            "title":     pygame.font.Font(None, 48),
            "huge":      pygame.font.Font(None, 64),
            "card_rank": pygame.font.Font(None, 32),
            "card_suit": pygame.font.Font(None, 44),
            "chip":      pygame.font.Font(None, 18),
            "result":    pygame.font.Font(None, 30),
        }

        self.seats = [Seat(i) for i in range(MAX_SEATS)]
        self.dealer_cards = []
        self.shoe = Shoe(6)

        self.state = ST_SEAT_SELECT
        self.active_seat = -1
        self.dealer_timer = 0

        self.status = ""
        self.status_timer = 0

        self.btns = {}

        self.dim = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.dim.fill(OVERLAY)

    # --- helpers ---
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

    def occ_seats(self):
        return [s for s in self.seats if s.occupied]

    def any_occ(self):
        return any(s.occupied for s in self.seats)

    # --- seat positions (arc) ---
    def seat_pos(self):
        """Return list of (cx, cy) for each of MAX_SEATS seats arranged in an arc."""
        positions = []
        # Arc parameters
        arc_cx = WIDTH // 2
        arc_cy = HEIGHT + 120
        arc_rx = 780
        arc_ry = 520
        # Distribute seats along an arc from ~150° to ~30° (bottom semicircle)
        start_angle = math.radians(150)
        end_angle = math.radians(30)
        n = MAX_SEATS
        for i in range(n):
            t = start_angle + (end_angle - start_angle) * i / max(1, n - 1)
            cx = arc_cx + int(arc_rx * math.cos(t))
            cy = arc_cy - int(arc_ry * math.sin(t))
            positions.append((cx, cy))
        return positions

    # --- card drawing ---
    def draw_card(self, card, x, y):
        r = pygame.Rect(x, y, CARD_W, CARD_H)
        if not card.face_up:
            rrect(self.display, (35, 45, 70), r, r=7)
            rrect(self.display, (55, 70, 105), r, r=7, bw=2)
            inner = pygame.Rect(x + 6, y + 6, CARD_W - 12, CARD_H - 12)
            rrect(self.display, (28, 38, 58), inner, r=4)
            rrect(self.display, (48, 62, 92), inner, r=4, bw=1)
            cx_c, cy_c = x + CARD_W // 2, y + CARD_H // 2
            pts = [(cx_c, cy_c - 18), (cx_c + 12, cy_c), (cx_c, cy_c + 18), (cx_c - 12, cy_c)]
            pygame.draw.polygon(self.display, (55, 70, 105), pts, 2)
            return

        sc = SUIT_COLORS.get(card.suit, WHITE)
        bg = (248, 244, 236) if card.suit in ("Hearts", "Diamonds") else (244, 244, 248)
        rrect(self.display, bg, r, r=7)
        rrect(self.display, (185, 185, 195), r, r=7, bw=1)
        sym = SUIT_SYM.get(card.suit, "?")

        rs = self.fonts["card_rank"].render(card.rank, True, sc)
        self.display.blit(rs, (x + 5, y + 4))
        ss_sm = self.fonts["small"].render(sym, True, sc)
        self.display.blit(ss_sm, (x + 5, y + 4 + rs.get_height()))
        ss_lg = self.fonts["card_suit"].render(sym, True, sc)
        self.display.blit(ss_lg, (x + CARD_W // 2 - ss_lg.get_width() // 2,
                                   y + CARD_H // 2 - ss_lg.get_height() // 2))
        rs2 = self.fonts["card_rank"].render(card.rank, True, sc)
        self.display.blit(rs2, (x + CARD_W - rs2.get_width() - 5, y + CARD_H - rs2.get_height() - 4))

    def draw_hand_cards(self, cards, cx, cy, max_w=240):
        if not cards:
            return
        n = len(cards)
        overlap = min(CARD_OVERLAP, (max_w - CARD_W) // max(1, n - 1)) if n > 1 else 0
        tw = CARD_W + (n - 1) * overlap
        sx = cx - tw // 2
        sy = cy - CARD_H // 2
        for i, c in enumerate(cards):
            self.draw_card(c, sx + i * overlap, sy)

    # --- chip drawing ---
    def draw_chip(self, val, x, y, rad=20):
        col = CHIP_COLORS.get(val, BLUE)
        pygame.draw.circle(self.display, col, (x, y), rad)
        pygame.draw.circle(self.display, WHITE, (x, y), rad, 2)
        pygame.draw.circle(self.display, col, (x, y), rad - 3)
        for a in range(0, 360, 45):
            r1 = rad - 5
            r2 = rad - 1
            x1 = x + int(r1 * math.cos(math.radians(a)))
            y1 = y + int(r1 * math.sin(math.radians(a)))
            x2 = x + int(r2 * math.cos(math.radians(a)))
            y2 = y + int(r2 * math.sin(math.radians(a)))
            pygame.draw.line(self.display, WHITE, (x1, y1), (x2, y2), 2)
        t = self.fonts["chip"].render(str(val), True, WHITE)
        self.display.blit(t, (x - t.get_width() // 2, y - t.get_height() // 2))

    def draw_bet_stack(self, bet, cx, cy):
        if bet <= 0:
            return
        chips = []
        rem = bet
        for v in sorted(CHIP_VALUES, reverse=True):
            while rem >= v:
                chips.append(v)
                rem -= v
        show = min(len(chips), 8)
        for i in range(show):
            self.draw_chip(chips[i], cx, cy - i * 3, rad=16)
        t = self.fonts["small"].render(f"${bet}", True, GOLD)
        self.display.blit(t, (cx - t.get_width() // 2, cy + 20))

    # --- table felt ---
    def draw_felt(self):
        felt = pygame.Rect(-300, 180, WIDTH + 600, HEIGHT + 300)
        pygame.draw.ellipse(self.display, DARK_GREEN, felt)
        pygame.draw.ellipse(self.display, FELT_BORDER, felt, 3)
        # Inner line
        inner = pygame.Rect(-200, 220, WIDTH + 400, HEIGHT + 200)
        pygame.draw.ellipse(self.display, FELT_GREEN, inner, 2)

    # --- dealer ---
    def draw_dealer(self):
        self.txt("DEALER", WIDTH // 2, 235, GOLD, "large", center=True)
        if self.dealer_cards:
            self.draw_hand_cards(self.dealer_cards, WIDTH // 2, 320, max_w=300)
            v, soft = hand_value(self.dealer_cards, only_visible=True)
            all_up = all(c.face_up for c in self.dealer_cards)
            if all_up:
                vt = f"Soft {v}" if soft and v <= 21 else str(v)
            else:
                vt = f"{v}+?"
            self.txt(vt, WIDTH // 2, 400, WHITE, "normal", center=True)

    # ===================================================================
    # SEAT SELECT
    # ===================================================================
    def draw_seat_select(self):
        self.display.fill(BG)

        self.txt("BLACKJACK", WIDTH // 2, 50, GOLD, "huge", center=True)
        self.txt("Select seats to play  •  Click to sit / leave", WIDTH // 2, 100, MUTED, "normal", center=True)

        positions = self.seat_pos()
        mx, my = pygame.mouse.get_pos()

        for i, (cx, cy) in enumerate(positions):
            seat = self.seats[i]
            r = pygame.Rect(cx - SEAT_W // 2, cy - SEAT_H // 2, SEAT_W, SEAT_H)
            hov = r.collidepoint(mx, my)

            if seat.occupied:
                bg, bord = (25, 55, 40), GREEN
            elif hov:
                bg, bord = (28, 36, 52), BLUE
            else:
                bg, bord = PANEL, BORDER

            rrect(self.display, bg, r, r=14)
            rrect(self.display, bord, r, r=14, bw=2 if (hov or seat.occupied) else 1)

            self.txt(f"SEAT {i+1}", cx, cy - 50, WHITE if seat.occupied else MUTED, "large", center=True)

            if seat.occupied:
                self.txt("SITTING", cx, cy, GREEN, "normal", center=True)
                self.txt(f"${seat.balance}", cx, cy + 30, TEAL, "normal", center=True)
                self.txt("Click to leave", cx, cy + 65, DIM, "small", center=True)
            else:
                pygame.draw.circle(self.display, DIM, (cx, cy + 5), 28, 2)
                self.txt("?", cx, cy + 5, DIM, "large", center=True)
                self.txt("Click to sit", cx, cy + 65, MUTED, "small", center=True)

        # Start button
        n = len(self.occ_seats())
        sr = pygame.Rect(WIDTH // 2 - 130, 150, 260, 52)
        can = n > 0
        bg = GREEN if can else CARD_GREY
        bord = (100, 220, 130) if can else BORDER
        tc = WHITE if can else DIM
        hov = sr.collidepoint(mx, my) and can
        if hov:
            bg = tuple(min(255, c + 30) for c in bg)
        rrect(self.display, bg, sr, r=10)
        rrect(self.display, bord, sr, r=10, bw=2 if hov else 1)
        self.txt(f"START GAME  ({n} seat{'s' if n != 1 else ''})", sr.centerx, sr.centery, tc, "normal", center=True)

        self.txt("ENTER to start  •  ESC to quit", WIDTH // 2, HEIGHT - 30, DIM, "small", center=True)

    # ===================================================================
    # BETTING
    # ===================================================================
    def draw_betting(self):
        self.display.fill(BG)
        self.draw_felt()
        self.draw_dealer()

        positions = self.seat_pos()
        mx, my = pygame.mouse.get_pos()

        for i, (cx, cy) in enumerate(positions):
            seat = self.seats[i]
            if not seat.occupied:
                continue

            has_bet = len(seat.hands) > 0 and seat.hands[0].bet > 0
            r = pygame.Rect(cx - SEAT_W // 2, cy - SEAT_H // 2, SEAT_W, SEAT_H)
            bg = (25, 48, 38) if has_bet else PANEL
            bord = GREEN if has_bet else BORDER
            rrect(self.display, bg, r, r=12)
            rrect(self.display, bord, r, r=12, bw=2 if has_bet else 1)

            self.txt(seat.name, cx, r.y + 16, WHITE, "normal", center=True)
            self.txt(f"Balance: ${seat.balance}", cx, r.y + 38, TEAL, "small", center=True)

            if has_bet:
                bet = seat.hands[0].bet
                self.draw_bet_stack(bet, cx, cy - 30)
                self.txt(f"Bet: ${bet}", cx, cy + 40, GOLD, "normal", center=True)
                # Clear button
                cr = pygame.Rect(cx - 38, cy + 58, 76, 26)
                ch = cr.collidepoint(mx, my)
                rrect(self.display, RED if ch else (80, 30, 30), cr, r=6)
                self.txt("Clear", cr.centerx, cr.centery, WHITE, "small", center=True)
            else:
                self.txt("Place Bet", cx, cy - 10, MUTED, "normal", center=True)

            # Chip row
            chip_y = r.bottom - 35
            csx = cx - (len(CHIP_VALUES) * 38) // 2 + 19
            for ci, cv in enumerate(CHIP_VALUES):
                ccx = csx + ci * 38
                ccy = chip_y
                dist = ((mx - ccx)**2 + (my - ccy)**2) ** 0.5
                rad = 19 if dist < 17 else 15
                self.draw_chip(cv, ccx, ccy, rad=rad)

        # Deal button
        all_bet = all(len(s.hands) > 0 and s.hands[0].bet > 0 for s in self.occ_seats())
        dr = pygame.Rect(WIDTH // 2 - 100, 155, 200, 50)
        can = all_bet and len(self.occ_seats()) > 0
        bg = GREEN if can else CARD_GREY
        bord = (100, 220, 130) if can else BORDER
        tc = WHITE if can else DIM
        hov = dr.collidepoint(mx, my) and can
        if hov:
            bg = tuple(min(255, c + 30) for c in bg)
        rrect(self.display, bg, dr, r=10)
        rrect(self.display, bord, dr, r=10, bw=2 if hov else 1)
        self.txt("DEAL", dr.centerx, dr.centery, tc, "large", center=True)

        # Back
        br = pygame.Rect(20, 20, 130, 34)
        hb = br.collidepoint(mx, my)
        rrect(self.display, PANEL2 if not hb else (40, 50, 70), br, r=8)
        rrect(self.display, BORDER, br, r=8, bw=1)
        self.txt("← Seats", br.centerx, br.centery, MUTED, "normal", center=True)

        self.txt("Click chips to bet  •  ENTER to deal  •  ESC for seats", WIDTH // 2, 120, DIM, "small", center=True)

    # ===================================================================
    # PLAYING (player turn, dealer turn, round over)
    # ===================================================================
    def draw_playing(self):
        self.display.fill(BG)
        self.draw_felt()
        self.draw_dealer()

        positions = self.seat_pos()

        for i, (cx, cy) in enumerate(positions):
            seat = self.seats[i]
            if not seat.occupied:
                continue

            is_active = (self.state == ST_PLAYER and i == self.active_seat)

            for hi, hand in enumerate(seat.hands):
                n_hands = len(seat.hands)
                if n_hands > 1:
                    hcx = cx + (hi - (n_hands - 1) / 2) * min(170, SEAT_W // n_hands)
                else:
                    hcx = cx
                hcy = cy - 30

                rw = SEAT_W - 20 if n_hands == 1 else SEAT_W // n_hands + 20
                r = pygame.Rect(hcx - rw // 2, hcy - CARD_H // 2 - 35, rw, SEAT_H - 30)
                is_cur = is_active and hi == seat.hand_idx

                if hand.result == "win" or hand.result == "blackjack":
                    bg, bord = (18, 48, 28), GREEN
                elif hand.result == "lose":
                    bg, bord = (48, 18, 18), RED
                elif hand.result == "push" or hand.result == "surrender":
                    bg, bord = (38, 38, 18), AMBER
                elif is_cur:
                    bg, bord = (22, 32, 52), BLUE
                else:
                    bg, bord = PANEL, BORDER

                rrect(self.display, bg, r, r=12)
                rrect(self.display, bord, r, r=12, bw=2 if is_cur else 1)

                if is_cur:
                    ind = pygame.Rect(r.x, r.y - 4, r.width, 4)
                    pygame.draw.rect(self.display, BLUE, ind,
                                     border_top_left_radius=12, border_top_right_radius=12)

                label = seat.name
                if n_hands > 1:
                    label += f" H{hi+1}"
                self.txt(label, hcx, r.y + 14, WHITE if is_cur else MUTED, "small", center=True)

                # Cards
                self.draw_hand_cards(hand.cards, hcx, hcy + 15, max_w=rw - 20)

                # Value
                v, soft = hand.val()
                if hand.busted():
                    vt, vc = f"BUST ({v})", RED
                elif hand.is_bj():
                    vt, vc = "BLACKJACK!", GOLD
                else:
                    vt = f"{'Soft ' if soft else ''}{v}"
                    vc = WHITE
                self.txt(vt, hcx, hcy + CARD_H // 2 + 25, vc, "small", center=True)

                # Bet
                self.txt(f"${hand.bet}", hcx, r.bottom - 45, GOLD, "small", center=True)

                # Result
                if hand.result:
                    rt = {
                        "win":       f"WIN +${hand.payout}",
                        "blackjack": f"BLACKJACK +${hand.payout}",
                        "lose":      f"LOSE",
                        "push":      "PUSH",
                        "surrender": "SURRENDER",
                    }.get(hand.result, "")
                    rc = {"win": GREEN, "blackjack": GOLD, "lose": RED,
                          "push": AMBER, "surrender": AMBER}.get(hand.result, WHITE)
                    self.txt(rt, hcx, r.bottom - 22, rc, "result", center=True)

            # Balance
            self.txt(f"${seat.balance}", cx, cy + SEAT_H // 2 - 20, TEAL, "small", center=True)

        # Action buttons
        if self.state == ST_PLAYER and 0 <= self.active_seat < MAX_SEATS:
            seat = self.seats[self.active_seat]
            hand = seat.cur_hand()
            if hand and not hand.done():
                self._draw_actions(seat, hand)

        if self.state == ST_ROUND_OVER:
            self._draw_round_btns()

        # Keyboard hints
        if self.state == ST_PLAYER:
            hints = [("H", "Hit"), ("S", "Stand"), ("D", "Double"), ("P", "Split"), ("R", "Surrender")]
            hx, hy = WIDTH - 155, 20
            hp = pygame.Rect(hx - 8, hy - 5, 150, len(hints) * 24 + 10)
            panel_box(self.display, hp, r=8)
            for ki, (key, desc) in enumerate(hints):
                kr = pygame.Rect(hx, hy + ki * 24, 24, 20)
                rrect(self.display, (32, 44, 62), kr, r=4)
                ks = self.fonts["small"].render(key, True, BLUE)
                self.display.blit(ks, (kr.x + kr.w // 2 - ks.get_width() // 2, kr.y + 2))
                self.txt(desc, hx + 30, hy + ki * 24 + 2, MUTED, "small")

        # Shoe
        self.txt(f"Shoe: {self.shoe.remaining()} cards", 20, HEIGHT - 28, DIM, "small")

    def _draw_actions(self, seat, hand):
        acts = [
            ("HIT",       GREEN,  True),
            ("STAND",     AMBER,  True),
            ("DOUBLE",    BLUE,   hand.can_double() and seat.balance >= hand.bet),
            ("SPLIT",     PURPLE, hand.can_split() and seat.balance >= hand.bet),
            ("SURRENDER", RED,    len(hand.cards) == 2 and len(seat.hands) == 1),
        ]
        bw, bh, gap = 120, 44, 10
        tw = len(acts) * bw + (len(acts) - 1) * gap
        sx = WIDTH // 2 - tw // 2
        by = 155
        self.btns = {}
        for idx, (label, color, en) in enumerate(acts):
            r = pygame.Rect(sx + idx * (bw + gap), by, bw, bh)
            b = Btn(r, label, color, en)
            b.draw(self.display, self.fonts)
            self.btns[label] = b

    def _draw_round_btns(self):
        self.btns = {}
        nr = Btn(pygame.Rect(WIDTH // 2 - 175, 155, 165, 50), "NEW ROUND", GREEN)
        nr.draw(self.display, self.fonts)
        self.btns["NEW_ROUND"] = nr

        cs = Btn(pygame.Rect(WIDTH // 2 + 10, 155, 165, 50), "CHANGE SEATS", BLUE)
        cs.draw(self.display, self.fonts)
        self.btns["CHANGE_SEATS"] = cs

    # ===================================================================
    # GAME LOGIC
    # ===================================================================
    def start_betting(self):
        self.state = ST_BETTING
        self.dealer_cards = []
        for s in self.occ_seats():
            s.reset()
            s.hands.append(Hand())
        self.btns = {}

    def place_bet(self, si, amt):
        seat = self.seats[si]
        if not seat.occupied or not seat.hands:
            return
        h = seat.hands[0]
        if seat.balance >= amt:
            h.bet += amt
            seat.balance -= amt

    def clear_bet(self, si):
        seat = self.seats[si]
        if not seat.occupied or not seat.hands:
            return
        h = seat.hands[0]
        seat.balance += h.bet
        h.bet = 0

    def deal_initial(self):
        occ = self.occ_seats()
        if not occ:
            return
        for s in occ:
            if not s.hands or s.hands[0].bet <= 0:
                self.set_status(f"{s.name} needs a bet!")
                return
        self.state = ST_DEALING
        for _ in range(2):
            for s in occ:
                s.hands[0].add(self.shoe.deal(True))
            if len(self.dealer_cards) == 0:
                self.dealer_cards.append(self.shoe.deal(True))
            else:
                self.dealer_cards.append(self.shoe.deal(False))
        self._start_player()

    def _start_player(self):
        self.state = ST_PLAYER
        self.active_seat = -1
        for s in self.occ_seats():
            for h in s.hands:
                if h.is_bj():
                    h.stood = True
            if not s.all_done():
                self.active_seat = s.idx
                break
        if self.active_seat == -1:
            self._start_dealer()

    def _advance(self):
        seat = self.seats[self.active_seat]
        h = seat.cur_hand()
        if h and h.done():
            if seat.advance():
                nh = seat.cur_hand()
                if nh and len(nh.cards) == 1:
                    nh.add(self.shoe.deal(True))
                if nh and not nh.done():
                    return
                # If this new hand is also done, keep advancing
                self._advance()
                return
        if seat.all_done():
            # Next seat
            found = False
            for s in self.occ_seats():
                if s.idx > self.active_seat and not s.all_done():
                    self.active_seat = s.idx
                    found = True
                    break
            if not found:
                self._start_dealer()

    def hit(self):
        seat = self.seats[self.active_seat]
        h = seat.cur_hand()
        if not h:
            return
        h.add(self.shoe.deal(True))
        if h.busted():
            self.set_status(f"{seat.name}: BUST!")
            h.stood = True
            self._advance()
        elif h.total() == 21:
            h.stood = True
            self._advance()

    def stand(self):
        seat = self.seats[self.active_seat]
        h = seat.cur_hand()
        if not h:
            return
        h.stood = True
        self._advance()

    def double(self):
        seat = self.seats[self.active_seat]
        h = seat.cur_hand()
        if not h or not h.can_double() or seat.balance < h.bet:
            return
        seat.balance -= h.bet
        h.bet *= 2
        h.doubled = True
        h.add(self.shoe.deal(True))
        h.stood = True
        self._advance()

    def split(self):
        seat = self.seats[self.active_seat]
        h = seat.cur_hand()
        if not h or not h.can_split() or seat.balance < h.bet:
            return
        nh = Hand()
        nh.bet = h.bet
        seat.balance -= h.bet
        nh.add(h.cards.pop())
        h.add(self.shoe.deal(True))
        nh.add(self.shoe.deal(True))
        idx = seat.hand_idx
        seat.hands.insert(idx + 1, nh)
        if h.is_bj() or h.total() == 21:
            h.stood = True
            self._advance()

    def surrender(self):
        seat = self.seats[self.active_seat]
        h = seat.cur_hand()
        if not h:
            return
        h.surrendered = True
        h.stood = True
        refund = h.bet // 2
        seat.balance += refund
        h.result = "surrender"
        self._advance()

    def _start_dealer(self):
        self.state = ST_DEALER
        for c in self.dealer_cards:
            c.face_up = True
        self.dealer_timer = 0

    def _dealer_step(self):
        alive = any(not h.busted() and not h.surrendered
                     for s in self.occ_seats() for h in s.hands)
        if not alive:
            return True
        v = hand_total(self.dealer_cards)
        if v < 17:
            self.dealer_cards.append(self.shoe.deal(True))
            return False
        return True

    def _resolve(self):
        self.state = ST_RESOLVE
        dv = hand_total(self.dealer_cards)
        dbj = is_blackjack(self.dealer_cards)
        dbust = dv > 21

        for s in self.occ_seats():
            for h in s.hands:
                if h.surrendered:
                    continue
                pv = h.total()
                pbj = h.is_bj()
                pb = pv > 21

                if pb:
                    h.result = "lose"
                    h.payout = 0
                elif pbj and dbj:
                    h.result = "push"
                    h.payout = 0
                    s.balance += h.bet
                elif pbj:
                    h.result = "blackjack"
                    h.payout = int(h.bet * 1.5)
                    s.balance += h.bet + h.payout
                elif dbust:
                    h.result = "win"
                    h.payout = h.bet
                    s.balance += h.bet * 2
                elif pv > dv:
                    h.result = "win"
                    h.payout = h.bet
                    s.balance += h.bet * 2
                elif pv == dv:
                    h.result = "push"
                    h.payout = 0
                    s.balance += h.bet
                else:
                    h.result = "lose"
                    h.payout = 0

        self.state = ST_ROUND_OVER
        self.btns = {}

    def new_round(self):
        for s in self.seats:
            if s.occupied and s.balance <= 0:
                s.occupied = False
                self.set_status(f"{s.name} is out of chips!")
        if not self.any_occ():
            self.state = ST_SEAT_SELECT
            return
        self.start_betting()

    # ===================================================================
    # EVENTS
    # ===================================================================
    def handle_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return False

            if self.state == ST_SEAT_SELECT:
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    self._ev_seat_click(e.pos)
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        return False
                    if e.key == pygame.K_RETURN and self.any_occ():
                        self.start_betting()

            elif self.state == ST_BETTING:
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    self._ev_bet_click(e.pos)
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        for s in self.occ_seats():
                            if s.hands:
                                s.balance += s.hands[0].bet
                        self.state = ST_SEAT_SELECT
                    elif e.key == pygame.K_RETURN:
                        self.deal_initial()

            elif self.state == ST_PLAYER:
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    self._ev_play_click(e.pos)
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_h:
                        self.hit()
                    elif e.key == pygame.K_s:
                        self.stand()
                    elif e.key == pygame.K_d:
                        self.double()
                    elif e.key == pygame.K_p:
                        self.split()
                    elif e.key == pygame.K_r:
                        self.surrender()

            elif self.state == ST_ROUND_OVER:
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    self._ev_round_click(e.pos)
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_RETURN:
                        self.new_round()
                    elif e.key == pygame.K_ESCAPE:
                        self.state = ST_SEAT_SELECT

        return True

    def _ev_seat_click(self, pos):
        positions = self.seat_pos()
        for i, (cx, cy) in enumerate(positions):
            r = pygame.Rect(cx - SEAT_W // 2, cy - SEAT_H // 2, SEAT_W, SEAT_H)
            if r.collidepoint(pos):
                self.seats[i].occupied = not self.seats[i].occupied
                if self.seats[i].occupied:
                    self.seats[i].balance = 1000
                return
        sr = pygame.Rect(WIDTH // 2 - 130, 150, 260, 52)
        if sr.collidepoint(pos) and self.any_occ():
            self.start_betting()

    def _ev_bet_click(self, pos):
        mx, my = pos
        # Back
        br = pygame.Rect(20, 20, 130, 34)
        if br.collidepoint(pos):
            for s in self.occ_seats():
                if s.hands:
                    s.balance += s.hands[0].bet
            self.state = ST_SEAT_SELECT
            return
        # Deal
        dr = pygame.Rect(WIDTH // 2 - 100, 155, 200, 50)
        all_bet = all(len(s.hands) > 0 and s.hands[0].bet > 0 for s in self.occ_seats())
        if dr.collidepoint(pos) and all_bet:
            self.deal_initial()
            return

        positions = self.seat_pos()
        for i, (cx, cy) in enumerate(positions):
            seat = self.seats[i]
            if not seat.occupied:
                continue
            r = pygame.Rect(cx - SEAT_W // 2, cy - SEAT_H // 2, SEAT_W, SEAT_H)

            # Clear
            if seat.hands and seat.hands[0].bet > 0:
                cr = pygame.Rect(cx - 38, cy + 58, 76, 26)
                if cr.collidepoint(pos):
                    self.clear_bet(i)
                    return

            # Chips
            chip_y = r.bottom - 35
            csx = cx - (len(CHIP_VALUES) * 38) // 2 + 19
            for ci, cv in enumerate(CHIP_VALUES):
                ccx = csx + ci * 38
                ccy = chip_y
                dist = ((mx - ccx)**2 + (my - ccy)**2) ** 0.5
                if dist < 19:
                    self.place_bet(i, cv)
                    return

    def _ev_play_click(self, pos):
        for name, btn in self.btns.items():
            if btn.hit(pos):
                {"HIT": self.hit, "STAND": self.stand, "DOUBLE": self.double,
                 "SPLIT": self.split, "SURRENDER": self.surrender}.get(name, lambda: None)()
                return

    def _ev_round_click(self, pos):
        for name, btn in self.btns.items():
            if btn.hit(pos):
                if name == "NEW_ROUND":
                    self.new_round()
                elif name == "CHANGE_SEATS":
                    self.state = ST_SEAT_SELECT
                return

    # ===================================================================
    # UPDATE & DRAW
    # ===================================================================
    def update(self):
        self.tick_status()
        if self.state == ST_DEALER:
            self.dealer_timer += 1
            if self.dealer_timer >= 30:
                self.dealer_timer = 0
                if self._dealer_step():
                    self._resolve()

    def draw(self):
        self.update()
        if self.state == ST_SEAT_SELECT:
            self.draw_seat_select()
        elif self.state == ST_BETTING:
            self.draw_betting()
        else:
            self.draw_playing()

        # Status bar
        if self.status:
            sr = pygame.Rect(WIDTH // 2 - 200, HEIGHT - 55, 400, 30)
            rrect(self.display, PANEL, sr, r=8)
            rrect(self.display, BORDER, sr, r=8, bw=1)
            col = GREEN if any(w in self.status for w in ("Win", "Bet", "Split")) else \
                  RED if any(w in self.status for w in ("BUST", "Lose", "out", "Not", "needs")) else WHITE
            self.txt(self.status, sr.centerx, sr.centery, col, "small", center=True)


# =====================
# Main
# =====================
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Blackjack")
    clock = pygame.time.Clock()
    game = BlackjackGame(screen)

    running = True
    while running:
        running = game.handle_events()
        game.draw()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
