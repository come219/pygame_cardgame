import os
import random
import pygame
import sys, subprocess

ACTIONS = ["shoot", "reload", "block"]

ASSET_DIR = os.path.join(os.path.dirname(__file__), "assets")
ACTION_IMAGES = {
    "shoot": "card_aa_shoot.png",
    "reload": "card_aa_reload.png",
    "block": "card_aa_block.png",
    "back": "card_aa_back.png",
}
SCREEN_SIZE = (1920, 1080) # 1280x720
CARD_SIZE = (140, 200)
CARD_Y = 360
BG_COLOR = (28, 30, 34)
TEXT_COLOR = (240, 240, 240)
FONT_SIZE = 28

HAND_SIZE = 7
START_HEALTH = 3
MAX_TURNS = 40


def make_deck():
    deck = ["shoot"] * 4 + ["reload"] * 4 + ["block"] * 4
    random.shuffle(deck)
    return deck


def draw_hand(deck, size=HAND_SIZE):
    hand = []
    for _ in range(min(size, len(deck))):
        hand.append(deck.pop())
    return hand

def draw_deck(deck, size=HAND_SIZE):
    return [deck.pop() for _ in range(min(size, len(deck)))]


def refill_hands(deck, player_hand, cpu_hand, size=HAND_SIZE):
    while deck and (len(player_hand) < size or len(cpu_hand) < size):
        if len(player_hand) < size:
            player_hand.append(deck.pop())
        if deck and len(cpu_hand) < size:
            cpu_hand.append(deck.pop())


def choose_cpu_card(hand, bullets):
    playable = [card for card in hand if card != "shoot" or bullets > 0]
    if not playable:
        playable = hand
    card = random.choice(playable)
    hand.remove(card)
    return card


def resolve_turn(p1_action, p2_action, p1_bullets, p2_bullets, p1_health, p2_health):
    p1_shoot = p1_action == "shoot" and p1_bullets > 0
    p2_shoot = p2_action == "shoot" and p2_bullets > 0
    p1_block = p1_action == "block"
    p2_block = p2_action == "block"

    if p1_action == "reload":
        p1_bullets += 1
    if p2_action == "reload":
        p2_bullets += 1
    if p1_shoot:
        p1_bullets -= 1
    if p2_shoot:
        p2_bullets -= 1

    if p1_shoot and not p2_block:
        p2_health -= 1
    if p2_shoot and not p1_block:
        p1_health -= 1

    winner = None
    if p2_health <= 0:
        winner = "player"
    elif p1_health <= 0:
        winner = "cpu"

    return p1_bullets, p2_bullets, p1_health, p2_health, winner


def load_card_images():
    images = {}
    for action, filename in ACTION_IMAGES.items():
        path = os.path.join(ASSET_DIR, filename)
        image = pygame.image.load(path).convert_alpha()
        images[action] = pygame.transform.smoothscale(image, CARD_SIZE)
    return images


def draw_text(surface, text, x, y, font, color=TEXT_COLOR):
    surface.blit(font.render(text, True, color), (x, y))


def draw_gun_duel_settings_dialog(screen, font):
    STARTING_PLAYER_HEALTH = 1
    MAX_STARTING_PLAYER_HEALTH = 10
    STARTING_BULLETS = 0
    MAX_STARTING_BULLETS = 3
    STARTING_HAND = 7
    MAX_STARTING_HAND = 7
    STARTING_PERK = False
    SHOPPING_PHASE = False
    CLASSIC_MODE = True

    clock = pygame.time.Clock()

    while True:
        screen.fill(BG_COLOR)
        draw_text(screen, "Gun Duel - Game Settings", 20, 20, font)
        draw_text(screen, "ESC - Close Settings", 20, 60, font)
        draw_text(screen, f"1. STARTING HP = {STARTING_PLAYER_HEALTH}", 20, 120, font)
        draw_text(screen, f"2. STARTING BULLETS = {STARTING_BULLETS}", 20, 180, font)
        draw_text(screen, f"3. STARTING HAND = {STARTING_HAND}", 20, 240, font)
        draw_text(screen, f"4. STARTING PERK = {'TRUE' if STARTING_PERK else 'FALSE'}", 20, 300, font)
        draw_text(screen, f"5. SHOPPING PHASE = {'ON' if SHOPPING_PHASE else 'OFF'}", 20, 360, font)
        draw_text(screen, f"6. CLASSIC MODE = {'ON' if CLASSIC_MODE else 'OFF'}", 20, 420, font)
        
        
        draw_text(screen, f"(MAX STARTING HP: {MAX_STARTING_PLAYER_HEALTH})", 40, 550, font)
        draw_text(screen, f"(MAX STARTING BULLETS: {MAX_STARTING_BULLETS})", 40, 610, font)
        draw_text(screen, f"(MAX STARTING HAND: {MAX_STARTING_HAND})", 40, 670, font)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        clock.tick(30)




def draw_screen(
    screen,
    font,
    card_images,
    player_hand,
    turn,
    p1_bullets,
    p1_health,
    p2_health,
    p2_bullets,
    cpu_action,
    player_action,
    message,
    winner,
):
    screen.fill(BG_COLOR)
    draw_text(screen, "ESC - MAINMENU", 20, 20, font)
    draw_text(screen, "Gun Duel - version 1.0", 420, 20, font)
    draw_text(screen, f"Turn {turn}", 20, 60, font)
    draw_text(screen, "TURN HISTORY", 1000, 20, font)
    draw_text(screen, "HOW TO PLAY?", 1000, 60, font)
    draw_text(screen, "GAME SETTINGS", 1000, 100, font)
    draw_text(screen, f"Player 1 | Health: {p1_health} | Bullets: {p1_bullets} | Hand: {len(player_hand)} | Deck: {len(player_hand)}  ", 20, 680, font)
    draw_text(screen, f"Player 1 played: {player_action or '...'}", 20, 270, font)
    draw_text(screen, f"Player 2 | Health: {p2_health} | Bullets: {p2_bullets} | Hand: {len(player_hand)}  | Deck: {len(player_hand)}  ", 20, 140, font)
    draw_text(screen, f"Player 2 played: {cpu_action or '...'}", 20, 200, font)
    draw_text(screen, message, 20, 580, font)
    if winner:
        draw_text(screen, "Game over. Close the window to exit.", 20, 560, font)

    for i, card in enumerate(player_hand):
        rect = pygame.Rect(40 + i * (CARD_SIZE[0] + 20), CARD_Y, *CARD_SIZE)
        screen.blit(card_images[card], rect)
        pygame.draw.rect(screen, TEXT_COLOR, rect, 2)
        draw_text(screen, str(i + 1), rect.x + 4, rect.y + 4, font)

    pygame.display.flip()    


def pygame_main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Gun Duel")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, FONT_SIZE)
    card_images = load_card_images()

    deck = make_deck()
    player_hand = draw_hand(deck)
    cpu_hand = draw_hand(deck)
    player_bullets = 0
    cpu_bullets = 0
    player_health = START_HEALTH
    cpu_health = START_HEALTH
    turn = 1
    cpu_action = None
    player_action = None
    message = "Click one of your cards to play."
    winner = None

    while True:
        if not winner:
            refill_hands(deck, player_hand, cpu_hand)
            if not player_hand and not cpu_hand and not deck:
                winner = "draw"
                message = "No cards left. The duel ends in a draw."

        draw_screen(
            screen,
            font,
            card_images,
            player_hand,
            turn,
            player_bullets,
            player_health,
            cpu_health,
            cpu_bullets,
            cpu_action,
            player_action,
            message,
            winner,
        )

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                import cardgame
                cardgame.main()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:    
                pygame.quit()
                subprocess.Popen(
                    [sys.executable, os.path.join(os.path.dirname(__file__), "cardgame.py")]
                )
                return
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                draw_gun_duel_settings_dialog(screen, font)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not winner:
                mx, my = event.pos
                for index, card in enumerate(player_hand):
                    rect = pygame.Rect(
                        40 + index * (CARD_SIZE[0] + 20), CARD_Y, *CARD_SIZE
                    )
                    if rect.collidepoint(mx, my):
                        if card == "shoot" and player_bullets == 0:
                            message = "You have no bullets to shoot."
                            cpu_action = None
                            break

                        player_action = player_hand.pop(index)
                        cpu_action = choose_cpu_card(cpu_hand, cpu_bullets)
                        (
                            player_bullets,
                            cpu_bullets,
                            player_health,
                            cpu_health,
                            winner,
                        ) = resolve_turn(
                            player_action,
                            cpu_action,
                            player_bullets,
                            cpu_bullets,
                            player_health,
                            cpu_health,
                        )

                        if winner == "player":
                            message = "You shot the CPU and won!"
                        elif winner == "cpu":
                            message = "CPU shot you and won!"
                        else:
                            turn += 1
                            if turn >= MAX_TURNS:
                                winner = "draw"
                                message = "The duel ends in a draw."
                            else:
                                message = (
                                    f"You played {player_action}. "
                                    f"CPU played {cpu_action}."
                                )
                        break

        clock.tick(30)


if __name__ == "__main__":
    pygame_main()
