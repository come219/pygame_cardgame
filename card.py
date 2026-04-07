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
        self.flipped = False
        self.offset_x = 0
        self.offset_y = 0

    def flip_card(self, new_image, screen, duration=500):
        """
        Animate the card flipping horizontally to change its image.

        :param new_image: the new image to display after flipping.
        :param screen: the pygame screen surface.
        :param duration: the duration of the flip animation in milliseconds.
        """
        clock = pygame.time.Clock()
        start_time = pygame.time.get_ticks()
        original_image = self.image

        

        while not self.flipped:
            elapsed_time = pygame.time.get_ticks() - start_time
            if elapsed_time > duration:
                self.flipped = True
                continue

            # Calculate the progress of the animation (0 to 1)
            progress = elapsed_time / duration

            # Determine the width of the card at this frame
            if progress <= 0.5:
                scale = 1 - 2 * progress  # Shrink
                current_image = original_image
            else:
                scale = 2 * (progress - 0.5)  # Expand
                current_image = new_image

            scaled_width = max(1, int(self.width * scale))
            scaled_image = pygame.transform.scale(current_image, (scaled_width, self.height))

            # Clear the area where the card is drawn
            screen.fill((0, 0, 0), (self.x, self.y, self.width, self.height))

            # Draw the scaled image centered at the original position
            screen.blit(scaled_image, (self.x + (self.width - scaled_width) // 2, self.y))

            pygame.display.flip()
            clock.tick(60)

        # Set the new image and dimensions after the animation
        self.image = new_image
        self.width = new_image.get_width()
        self.height = new_image.get_height()
    
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

    def moveto(self, new_x, new_y, screen, duration=500):
        """
        Animate the card moving from its current position to a new position.

        :param new_x: the target x-coordinate.
        :param new_y: the target y-coordinate.
        :param screen: the pygame screen surface.
        :param duration: the duration of the move animation in milliseconds.
        """
        clock = pygame.time.Clock()
        start_time = pygame.time.get_ticks()
        start_x, start_y = self.x, self.y

        while True:
            elapsed_time = pygame.time.get_ticks() - start_time
            if elapsed_time >= duration:
                # Stop moving after reaching the target
                break

            # Calculate the progress of the animation (0 to 1)
            progress = min(1, elapsed_time / duration)

            # Interpolate the position
            current_x = start_x + (new_x - start_x) * progress
            current_y = start_y + (new_y - start_y) * progress

            # Clear the area where the card is drawn
            screen.fill((0, 0, 0), (self.x, self.y, self.width, self.height))

            # Update the position and draw the card
            self.x, self.y = current_x, current_y
            self.draw(screen)

            pygame.display.flip()
            clock.tick(60)

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
