import pygame

WIDTH = 1920
HEIGHT = 1080

class card:
    def __init__(self, card_type, image, x, y):
        """
        initialize a card object.

        :param card_type: the type of the card (e.g., "rock", "paper", "scissors").
        :param image: the image of the card.
        :param x: the x-coordinate of the card on the screen.
        :param y: the y-coordinate of the card on the screen.
        """
        self.card_type = card_type
        self.image = image
        self.x = x
        self.y = y
        self.width = image.get_width()
        self.height = image.get_height()
        self.selected = False
        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0

    def draw(self, screen):
        """
        draw the card on the screen.

        :param screen: the pygame screen surface.
        """
        screen.blit(self.image, (self.x, self.y))

    def is_clicked(self, mouse_pos):
        """
        check if the card is clicked.

        :param mouse_pos: the position of the mouse click.
        :return: true if the card is clicked, false otherwise.
        """
        mouse_x, mouse_y = mouse_pos

        # if self.dragging:
        #     # Check if the card is within the snapping field
        #     field_rect = pygame.Rect(WIDTH / 2 - 350, HEIGHT / 2 - 180, 800, 420)
        #     if field_rect.collidepoint(mouse_x, mouse_y):
        #         self.x = field_rect.x + (field_rect.width - self.width) // 2
        #         self.y = field_rect.y + (field_rect.height - self.height) // 2
        #         self.dragging = False

        return self.x <= mouse_x <= self.x + self.width and self.y <= mouse_y <= self.y + self.height

    def select(self):
        """
        mark the card as selected.
        """
        self.selected = True

    def deselect(self):
        """
        mark the card as not selected.
        """
        self.selected = False

    def position(self, x=None, y=None):
        """
        get or set the position of the card.

        :param x: the new x-coordinate of the card (optional).
        :param y: the new y-coordinate of the card (optional).
        :return: a tuple (x, y) representing the current position if no arguments are provided.
        """
        if x is not None and y is not None:
            self.x = x
            self.y = y
        return self.x, self.y

    def handle_event(self, event):
        """
        Handle mouse events for dragging the card.

        :param event: the pygame event.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_clicked(event.pos):
                self.dragging = True
                self.offset_x = event.pos[0] - self.x
                self.offset_y = event.pos[1] - self.y

        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.x = event.pos[0] - self.offset_x
                self.y = event.pos[1] - self.offset_y
