# gun duel game
# two players can: shoot, reload, or block

import random


ACTIONS = ["shoot", "reload", "block"]


def make_deck():
    deck = ["shoot"] * 4 + ["reload"] * 4 + ["block"] * 4
    random.shuffle(deck)
    return deck


def draw_hand(deck, size=5):
    hand = []
    for _ in range(size):
        if deck:
            hand.append(deck.pop())
    return hand


def choose_player_card(hand, bullets):
    while True:
        print("\nYour hand:")
        for idx, card in enumerate(hand, start=1):
            print(f"{idx}. {card}")
        choice = input("Choose a card by number: ").strip()
        if not choice.isdigit():
            print("Enter a number.")
            continue
        index = int(choice) - 1
        if not 0 <= index < len(hand):
            print("Invalid selection.")
            continue
        card = hand[index]
        if card == "shoot" and bullets == 0:
            print("You have no bullets to shoot.")
            continue
        return hand.pop(index)


def choose_cpu_card(hand, bullets):
    playable = [card for card in hand if card != "shoot" or bullets > 0]
    if not playable:
        playable = hand
    card = random.choice(playable)
    hand.remove(card)
    return card


def resolve_turn(p1_action, p2_action, p1_bullets, p2_bullets):
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

    winner = None
    if p1_shoot and not p2_block:
        winner = "player"
    elif p2_shoot and not p1_block:
        winner = "cpu"
    return p1_bullets, p2_bullets, winner


def display_state(turn, p1_bullets, p2_bullets):
    print(f"\n--- Turn {turn} ---")
    print(f"Your bullets: {p1_bullets}")
    print(f"CPU bullets: {p2_bullets}")


def main():
    deck = make_deck()
    player_hand = draw_hand(deck)
    cpu_hand = draw_hand(deck)
    player_bullets = 0
    cpu_bullets = 0
    turn = 1

    while True:
        if not player_hand:
            player_hand = draw_hand(deck)
        if not cpu_hand:
            cpu_hand = draw_hand(deck)
        display_state(turn, player_bullets, cpu_bullets)

        player_action = choose_player_card(player_hand, player_bullets)
        cpu_action = choose_cpu_card(cpu_hand, cpu_bullets)
        print(f"CPU plays: {cpu_action}")

        player_bullets, cpu_bullets, winner = resolve_turn(
            player_action, cpu_action, player_bullets, cpu_bullets
        )

        if winner:
            if winner == "player":
                print("You shot the CPU and won!")
            else:
                print("CPU shot you and won!")
            break

        if turn >= 40:
            print("The duel ends in a draw.")
            break

        turn += 1


if __name__ == "__main__":
    main()