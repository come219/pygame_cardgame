import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions 800x600 
display_Width = 1920
display_Height = 1080
WIDTH, HEIGHT = display_Width, display_Height
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Balanced Card Game | Rock Paper Scissors")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Font
font = pygame.font.SysFont(None, 50)

# Choices
choices = ["Rock", "Paper", "Scissors"]

# Load images
rock_img = pygame.image.load("assets/card_rock.png")
paper_img = pygame.image.load("assets/card_paper.png")
scissors_img = pygame.image.load("assets/card_scissors.png")

# Scale images
rock_img = pygame.transform.scale(rock_img, (150, 150))
paper_img = pygame.transform.scale(paper_img, (150, 150))
scissors_img = pygame.transform.scale(scissors_img, (150, 150))

# Function to display text
def display_text(text, color, x, y):
    screen_text = font.render(text, True, color)
    screen.blit(screen_text, (x, y))

# Function to determine the winner
def determine_winner(player, computer):
    if player == computer:
        return "Draw"
    elif (player == "Rock" and computer == "Scissors") or \
         (player == "Paper" and computer == "Rock") or \
         (player == "Scissors" and computer == "Paper"):
        return "Player Wins"
    else:
        return "Computer Wins"


def start_full_game():
    main()


# Main game loop
def main():
    running = True
    player_choice = None
    computer_choice = None
    result = None

    while running:
        screen.fill(BLACK)

        # Display choices
        screen.blit(rock_img, (100, 400))
        screen.blit(paper_img, (325, 400))
        screen.blit(scissors_img, (550, 400))

        display_text("Choose: Rock, Paper, or Scissors", WHITE, 150, 50)

        if result:
            display_text(f"Player: {player_choice}", BLUE, 50, 200)
            display_text(f"Computer: {computer_choice}", RED, 50, 250)
            display_text(result, GREEN, 50, 300)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    import cardgame  # Import the cardgame module
                    cardgame.main()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 100 <= x <= 250 and 400 <= y <= 550:
                    player_choice = "Rock"
                elif 325 <= x <= 475 and 400 <= y <= 550:
                    player_choice = "Paper"
                elif 550 <= x <= 700 and 400 <= y <= 550:
                    player_choice = "Scissors"

                if player_choice:
                    computer_choice = random.choice(choices)
                    result = determine_winner(player_choice, computer_choice)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()