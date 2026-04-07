import pygame


# assets/deck_a_image.png


# =====================
# Constants
# =====================
WIDTH, HEIGHT = 1920, 1080

BLACK       = (20, 20, 20)
WHITE       = (255, 255, 255)
RED         = (220, 60, 60)
BLUE        = (80, 140, 255)
GREY        = (70, 70, 70)
HOVER       = (120, 120, 120)
DARK_GREY   = (100, 100, 100)
NEW_BLUE    = (80, 160, 220)

CARD_W, CARD_H  = 100, 130
MAX_DECK_SIZE   = 30
STATUS_DURATION = 120   # frames before status clears (~2s at 60fps)


# =====================
# Deck Manager
# =====================
class DeckManager:
    def __init__(self, display):
        self.display = display
        self.font       = pygame.font.Font(None, 28)
        self.font_small = pygame.font.Font(None, 22)
        self.font_large = pygame.font.Font(None, 42)

        # collection = unique card types available
        # owned_cards = how many copies the player owns of each
        self.collection = [
            "Rock", "Paper", "Scissors",
            "Fire", "Water", "Wind",
            "Knight", "Archer", "Mage",
            "Dragon", "Goblin", "Shield"
        ]
        self.owned_cards = {card: 2 for card in self.collection}  # default: 2 copies each

        # Deck = dict (stacking)
        self.deck = {}

        # Undo
        self.undo_stack = []

        # Dragging
        self.dragging_card = None
        self.drag_from = None   # "collection" or "deck"
        self.drag_pos  = (0, 0)

        # Status message + timer
        self.status        = ""
        self.status_timer  = 0

        # Layout
        # FIX 5: deck_pos now has 30 slots to match MAX_DECK_SIZE
        self.collection_pos = self.grid(50, 530, 12)
        self.deck_pos       = self.grid(50, 120, MAX_DECK_SIZE)

    # =====================
    def grid(self, x, y, count):
        return [(x + (i % 10) * 110, y + (i // 10) * 140) for i in range(count)]

    # =====================
    # Events
    # =====================
    def handle_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return False

            elif e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 3:
                    self._right_click(pygame.mouse.get_pos())
                else:
                    self.start_drag(pygame.mouse.get_pos())

            elif e.type == pygame.MOUSEBUTTONUP:
                self.end_drag(pygame.mouse.get_pos())

            elif e.type == pygame.MOUSEMOTION:
                self.drag_pos = pygame.mouse.get_pos()

            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    import cardgame
                    cardgame.main()  # go back to main menu
                
                elif e.key == pygame.K_v:
                    print("View all cards!")
                    import card_viewer
                    card_viewer.main()

                elif e.key == pygame.K_d:
                    print("View all decks!")
                

                elif e.key == pygame.K_z:
                    self.undo()
                elif e.key == pygame.K_c:
                    self.clear_deck()

        return True

    def _right_click(self, pos):
        """Right-click on collection = add one copy to deck (if copies available). Right-click on deck = remove one copy back to owned pool."""
        # Check collection first
        for i, p in enumerate(self.collection_pos):
            if i < len(self.collection) and self.inside(pos, p):
                card = self.collection[i]
                if self.total_cards() >= MAX_DECK_SIZE:
                    self.set_status("Deck Full!")
                elif self.copies_available(card) <= 0:
                    self.set_status(f"No copies left!")
                else:
                    self.push_undo()
                    self.add_card(card)
                    self.set_status(f"Added {card}  ({self.copies_available(card)} left)")
                return

        # Check deck cards
        deck_list = self.expand_deck()
        for i, p in enumerate(self.deck_pos):
            if i < len(deck_list) and self.inside(pos, p):
                self.remove_card(deck_list[i])
                return

    # =====================
    # Drag Logic
    # =====================
    def start_drag(self, pos):
        # From collection — only allow drag if copies are available
        for i, p in enumerate(self.collection_pos):
            if i < len(self.collection) and self.inside(pos, p):
                card = self.collection[i]
                if self.copies_available(card) > 0:
                    self.dragging_card = card
                    self.drag_from = "collection"
                else:
                    self.set_status(f"No copies left!")
                return

        # FIX 2: save undo state here only once, not again in remove_card
        deck_list = self.expand_deck()
        for i, p in enumerate(self.deck_pos):
            if i < len(deck_list) and self.inside(pos, p):
                self.dragging_card = deck_list[i]
                self.drag_from = "deck"
                self.push_undo()
                # Directly manipulate deck without triggering another push_undo
                self.deck[deck_list[i]] -= 1
                if self.deck[deck_list[i]] <= 0:
                    del self.deck[deck_list[i]]
                return

    def end_drag(self, pos):
        if not self.dragging_card:
            return

        dropped_in_deck = False
        for p in self.deck_pos:
            if self.inside(pos, p):
                dropped_in_deck = True
                break

        if dropped_in_deck:
            if self.total_cards() >= MAX_DECK_SIZE:
                self.set_status("Deck Full!")
                # If dragged from deck and can't re-add, restore the card
                if self.drag_from == "deck":
                    self.deck[self.dragging_card] = self.deck.get(self.dragging_card, 0) + 1
            else:
                if self.drag_from == "collection":
                    self.push_undo()
                self.add_card(self.dragging_card)
                self.set_status(f"Added {self.dragging_card}")
        else:
            # Dropped outside deck — if it came from deck, restore it
            if self.drag_from == "deck":
                self.deck[self.dragging_card] = self.deck.get(self.dragging_card, 0) + 1
                self.set_status(f"Cancelled")

        self.dragging_card = None
        self.drag_from = None

    # =====================
    # Deck Logic
    # =====================
    def add_card(self, card):
        self.deck[card] = self.deck.get(card, 0) + 1

    def remove_card(self, card):
        if card and card in self.deck:
            self.push_undo()
            self.deck[card] -= 1
            if self.deck[card] <= 0:
                del self.deck[card]
            self.set_status(f"Removed {card}")

    def clear_deck(self):
        if self.deck:
            self.push_undo()
            self.deck = {}
            self.set_status("Deck Cleared!")

    def expand_deck(self):
        result = []
        for card, count in self.deck.items():
            result.extend([card] * count)
        return result

    def total_cards(self):
        return sum(self.deck.values())
    
    def deck_name(self):
        return "My Deck"

    def copies_available(self, card):
        """Owned copies minus how many are already in the deck."""
        owned = self.owned_cards.get(card, 0)
        in_deck = self.deck.get(card, 0)
        return owned - in_deck

    def push_undo(self):
        self.undo_stack.append(self.deck.copy())
        if len(self.undo_stack) > 50:
            self.undo_stack.pop(0)

    def undo(self):
        if self.undo_stack:
            self.deck = self.undo_stack.pop()
            self.set_status("Undo!")
            

    # FIX 3: status now has a timer so it clears automatically
    def set_status(self, msg):
        self.status       = msg
        self.status_timer = STATUS_DURATION

    def tick_status(self):
        if self.status_timer > 0:
            self.status_timer -= 1
            if self.status_timer == 0:
                self.status = ""

    # =====================
    # Drawing
    # =====================
    def draw_card(self, card, pos, in_deck=False, greyed=False):
        mouse = pygame.mouse.get_pos()
        if greyed:
            color = (40, 40, 40)
        else:
            color = HOVER if self.inside(mouse, pos) else GREY

        pygame.draw.rect(self.display, color, (*pos, CARD_W, CARD_H))
        pygame.draw.rect(self.display, WHITE, (*pos, CARD_W, CARD_H), 2)

        self.draw_text(card, pos[0] + 8, pos[1] + 55)

        # FIX 4: only show stack count badge on deck cards, not collection cards
        if in_deck and card in self.deck and self.deck[card] > 1:
            self.draw_text(f"x{self.deck[card]}", pos[0] + 62, pos[1] + 6, RED)

    def draw_text(self, text, x, y, color=WHITE, font=None):
        f = font or self.font
        surf = f.render(text, True, color)
        self.display.blit(surf, (x, y))

    def draw_sidebar(self):
        """Keyboard shortcut panel (changeDeckMenu style)."""
        sx = 1400
        self.draw_text("Deck Manager",        20, 20,  DARK_GREY, self.font_large)
        self.draw_text("Press ESC to return to main menu",   sx, 30, NEW_BLUE)
        
        
        
        self.draw_text("Press V to view all cards", sx, 80, NEW_BLUE)
        self.draw_text("Press D to view all decks", sx, 130, NEW_BLUE)
        self.draw_text("Press Q to view full collection", sx, 180, NEW_BLUE)

        self.draw_text("Press Z to undo",     sx, 230, NEW_BLUE)
        self.draw_text("Press C to clear",    sx, 280, NEW_BLUE)
        
        self.draw_text("Right-click collection to add", sx, 330, NEW_BLUE)
        self.draw_text("Right-click deck to remove",   sx, 380, NEW_BLUE)
        self.draw_text("Drag from collection to add",  sx, 430, NEW_BLUE)

        # Undo stack depth
        self.draw_text(f"Undo history: {len(self.undo_stack)}", sx, 460, DARK_GREY, self.font_small)

        # Status message
        if self.status:
            self.draw_text(self.status, sx, 520, WHITE)

    def draw(self):
        self.tick_status()  # FIX 3: advance status timer each frame

        self.display.fill(BLACK)

        # Section headers (changeDeckMenu style)
        self.draw_text(f"DECK: {self.deck_name()}", 50, 80, RED)
        self.draw_text(f"CARDS: {self.total_cards()}/{MAX_DECK_SIZE}", 350, 80, RED)
        self.draw_text(f"(UNSAVED)", 550, 80, RED)
        self.draw_text("COLLECTION", 50, 500, DARK_GREY)
        self.draw_text(f"Cards: {len(self.collection)}", 200, 500, DARK_GREY, self.font_small)

        # Draw deck cards
        deck_list = self.expand_deck()
        for i, card in enumerate(deck_list):
            if i < len(self.deck_pos):
                self.draw_card(card, self.deck_pos[i], in_deck=True)

        # Draw collection cards
        for i, card in enumerate(self.collection):
            if i < len(self.collection_pos):
                p = self.collection_pos[i]
                available = self.copies_available(card)
                self.draw_card(card, p, in_deck=False, greyed=available <= 0)
                owned = self.owned_cards.get(card, 0)
                in_deck = self.deck.get(card, 0)
                # Show "in_deck / owned" below card name
                self.draw_text(f"{in_deck}/{owned}", p[0] + 8, p[1] + 75, RED if in_deck >= owned else DARK_GREY, self.font_small)

        # Drag preview
        if self.dragging_card:
            pygame.draw.rect(self.display, BLUE, (*self.drag_pos, CARD_W, CARD_H))
            pygame.draw.rect(self.display, WHITE, (*self.drag_pos, CARD_W, CARD_H), 2)
            self.draw_text(self.dragging_card, self.drag_pos[0] + 8, self.drag_pos[1] + 55)

        self.draw_sidebar()

    # =====================
    def inside(self, pos, rect):
        x, y = pos
        rx, ry = rect
        return rx <= x <= rx + CARD_W and ry <= y <= ry + CARD_H


# =====================
# Main
# =====================
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
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