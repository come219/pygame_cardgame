import pygame
import random
from card import card

class Deck:
    def __init__(self, card_num, card_images, back_image, deck_position):
        """
        Initializes the deck object.

        :param card_types: list of strings, e.g. ["Rock", "Rock", "Paper", ...]
        :param card_images: dict mapping card type to its image
        :param back_image: pygame Surface for the card back image
        :param deck_position: (x, y) tuple for where to render the deck
        """
        self.card_num = card_num
        self.card_images = card_images
        self.back_image = back_image
        self.deck_img = pygame.transform.scale(back_image, (150, 150))
        self.deck_x, self.deck_y = deck_position
        self.width = 150
        self.height = 150

    def draw_from_deck(self):
        """Pops a card type from the deck."""
        if self.cards:
            return self.cards.pop(random.randrange(len(self.cards)))
        return None

    def draw_card_object(self, screen):
        """
        Draws a card object from the deck with animation (flip and move).
        :param screen: Pygame surface to draw to.
        :return: card object or None
        """
        card_type = self.draw_from_deck()
        if card_type:
            card_obj = card(card_type, self.back_image, self.deck_x, self.deck_y)
            card_obj.card_type_image = self.card_images[card_type]
            card_obj.flip_card(card_obj.card_type_image, screen)
            return card_obj
        return None

    def draw_deck_image(self, screen, font, text_color):
        """
        Displays the deck image and count on the screen.
        :param screen: Pygame surface
        :param font: Pygame font object
        :param text_color: color for the text
        """
        # Draw the deck image
        screen.blit(self.deck_img, (self.deck_x, self.deck_y))

        # Draw the number of cards remaining
        text = font.render(f"Player Deck: {len(self.card_num)}", True, text_color)
        screen.blit(text, (self.deck_x+20, self.deck_y+10))
