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

image_path = "assets/ladder_level0.png"
image_path_claimed = "assets/ladder_level0_claimed.png"

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

    claimed = False

    while running:
        screen.fill(BLACK)
        pygame.draw.rect(screen, DARK_GREY, (0, 0, WIDTH, 50))
        
        # Display choices
        screen.blit(rock_img, (     WIDTH/2 - 500 + 100, HEIGHT - 700))
        screen.blit(paper_img, (    WIDTH/2 - 500 + 325, HEIGHT - 700))
        screen.blit(scissors_img, ( WIDTH/2 - 500 + 550, HEIGHT - 700))
        

        display_text("Menu", GREY, 20, 4)
        pygame.draw.rect(screen, GREY, (WIDTH / 2 - 180, 150, 150, 150))
        
        ladder_image = pygame.image.load(image_path)
        ladder_image = pygame.transform.scale(ladder_image, (150, 150))

        ladder_image_claimed = pygame.image.load(image_path_claimed)
        ladder_image_claimed = pygame.transform.scale(ladder_image_claimed, (150, 150))

        if not claimed:
            screen.blit(ladder_image, (WIDTH / 2 - 180, 150,))
        else:
            screen.blit(ladder_image_claimed, (WIDTH / 2 - 180, 150,))

        display_text("Ladder Level 0: Grandpa's Cards", GREY, WIDTH /2 - 200, 4)
        display_text('"Here are your cards,', WHITE, WIDTH /2, 200)

        if rand_bool1 == True:
            display_text('Take good care of them!"', WHITE, WIDTH/2, 250)
        elif rand_bool2 == True:
            display_text("Don't lose 'em!", WHITE, WIDTH/2, 250)
        elif rand_bool3 == True:
            display_text("I've never lost with these!", WHITE, WIDTH/2, 250)
        elif rand_bool4 == True:
            display_text('Believe in them."', WHITE, WIDTH/2, 250)
        elif rand_bool5 == True:
            display_text('Rock, Paper and Scissors."', WHITE, WIDTH/2, 250)
        else:
            display_text('ROCK, PAPER & SCISSORS!"', WHITE, WIDTH/2, 250)


        if not claimed:
            display_text(f"Press SPACE to claim your cards!", LIGHT_BLUE, WIDTH/2 - 100, HEIGHT / 2 + 50)

        if claimed:
            display_text(f"Player: (PLAYER_NAME)", LIGHT_BLUE, WIDTH/2 - 100, HEIGHT / 2 + 50)
            display_text(f"Recieved: ", GREY, WIDTH/2 - 100, HEIGHT / 2 + 100)
            display_text(f"x1 Rock", GREY, WIDTH/2 + 50, HEIGHT / 2 + 150)
            display_text(f"x1 Paper", GREY, WIDTH/2 + 50, HEIGHT / 2 + 200)
            display_text(f"x1 Scissors", GREY, WIDTH/2 + 50, HEIGHT / 2 + 250)
    


        if claimed:
            # Draw Next button
            next_rect = pygame.draw.rect(screen, GREY, (WIDTH/2, HEIGHT - 150, 140, 50))
            display_text("Next", WHITE, WIDTH/2, HEIGHT - 150)
        else:
            # Draw Claim button
            claim_rect = pygame.draw.rect(screen, GREY, (WIDTH/2, HEIGHT - 150, 140, 50))
            display_text("Claim", WHITE, WIDTH/2, HEIGHT - 150)

        


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    import cardgame  # Import the cardgame module
                    cardgame.main()
                if event.key == pygame.K_n:
                    running = False
                    import ladder_level1  # Import the cardgame module
                    ladder_level1.main()

                if event.key == pygame.K_SPACE and not claimed:
                    claimed = True
                

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                if claim_rect.collidepoint(x, y):
                    # Handle claim action
                    pass
                elif next_rect.collidepoint(x, y):
                    # Handle next action
                    pass


        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()