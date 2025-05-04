import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions 800x600 
display_Width = 1920
display_Height = 1080
WIDTH, HEIGHT = display_Width, display_Height
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Balanced Card Game | Story Mode 1")

# Colors
WHITE = (255, 255, 255)
GREY=  (128,128,128)
DARK_GREY= (69,69,69)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (173, 216, 230)


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
    player_wins = 0
    computer_choice = None
    computer_wins = 0
    num_draws = 0
    result = None
    rand_bool1 = random.getrandbits(1)
    rand_bool2 = random.getrandbits(1)
    rand_bool3 = random.getrandbits(1)
    rand_bool4 = random.getrandbits(1)
    rand_bool5 = random.getrandbits(1)

    while running:
        screen.fill(BLACK)
        pygame.draw.rect(screen, DARK_GREY, (0, 0, WIDTH, 50))
        
        # Display choices
        screen.blit(rock_img, (     WIDTH/2 - 500 + 100, HEIGHT - 200))
        screen.blit(paper_img, (    WIDTH/2 - 500 + 325, HEIGHT - 200))
        screen.blit(scissors_img, ( WIDTH/2 - 500 + 550, HEIGHT - 200))

        display_text("Menu", GREY, 20, 4)
        pygame.draw.rect(screen, GREY, (WIDTH / 2 - 180, 150, 150, 150))
        display_text("Ladder Level 1: Rock, Paper, or Scissors Guy", GREY, WIDTH /2 - 200, 4)
        display_text('"Best of 3? Good luck!', WHITE, WIDTH /2, 200)

        if rand_bool1 == True:
            display_text('Rock, Paper, or Scissors?"', WHITE, WIDTH/2, 250)
        elif rand_bool2 == True:
            display_text('Paper, Rock, or Scissors?"', WHITE, WIDTH/2, 250)
        elif rand_bool3 == True:
            display_text('Paper, Scissors, or Rock?"', WHITE, WIDTH/2, 250)
        elif rand_bool4 == True:
            display_text('Scissors, Paper, or Rock?"', WHITE, WIDTH/2, 250)
        elif rand_bool5 == True:
            display_text('Rock, Scissors, or Paper?"', WHITE, WIDTH/2, 250)
        else:
            display_text('Rock, Paper, or Scissors?"', WHITE, WIDTH/2, 250)

        display_text(f"Wins: {player_wins}", LIGHT_BLUE, WIDTH/2 - 100, HEIGHT / 2 + 150)
        display_text(f"Wins: {computer_wins}", RED, WIDTH/2 - 100, HEIGHT / 2 - 150)
        display_text(f"Player: {player_choice}", LIGHT_BLUE, WIDTH/2 - 100, HEIGHT / 2 + 100)
        display_text(f"Enemy: {computer_choice}", RED, WIDTH/2 - 100, HEIGHT / 2 - 100)
        display_text(f"Draws: {num_draws}", BLUE, WIDTH/2 - 300, HEIGHT/2)
        if result:
            display_text(result, GREEN, WIDTH/2, HEIGHT/2)



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
                if WIDTH/2 - 500 + 100 <= x <= WIDTH/2 - 500 + 250 and HEIGHT - 200 <= y <= HEIGHT - 50:
                    player_choice = "Rock"
                elif WIDTH/2 - 500 + 325 <= x <= WIDTH/2 - 500 + 475 and HEIGHT - 200 <= y <= HEIGHT - 50:
                    player_choice = "Paper"
                elif WIDTH/2 - 500 + 550 <= x <= WIDTH/2 - 500 + 700 and HEIGHT - 200 <= y <= HEIGHT - 50:
                    player_choice = "Scissors"

                if player_choice:
                    computer_choice = random.choice(choices)
                    result = determine_winner(player_choice, computer_choice)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()