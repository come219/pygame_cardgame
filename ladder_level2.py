import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions 800x600 
display_Width = 1920
display_Height = 1080
WIDTH, HEIGHT = display_Width, display_Height
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Balanced Card Game | Story Mode 2")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (128,128,128)
DARK_GREY = (69,69,69)

# Font
font = pygame.font.SysFont(None, 50)

# Choices
choices = ["Rock", "Paper", "Scissors", "Spock", "Lizard"]

# Load images
game_img = pygame.image.load("assets/help_lizard_spock.png")
rock_img = pygame.image.load("assets/card_rock.png")
paper_img = pygame.image.load("assets/card_paper.png")
scissors_img = pygame.image.load("assets/card_scissors.png")
spock_img = pygame.image.load("assets/card_spock.png")
lizard_img = pygame.image.load("assets/card_lizard.png")

# Scale images
game_img = pygame.transform.scale(game_img, (500, 500))
rock_img = pygame.transform.scale(rock_img, (150, 150))
paper_img = pygame.transform.scale(paper_img, (150, 150))
scissors_img = pygame.transform.scale(scissors_img, (150, 150))
spock_img = pygame.transform.scale(spock_img, (150, 150))
lizard_img = pygame.transform.scale(lizard_img, (150, 150))

# Function to display text
def display_text(text, color, x, y):
    screen_text = font.render(text, True, color)
    screen.blit(screen_text, (x, y))

# Function to determine the winner
def determine_winner(player, computer):
    global computer_wins, b_computer_win, b_player_win, b_draw, player_wins, draw_num
    if player == computer:
        b_draw = True
        b_player_win = False
        b_computer_win = False
        draw_num+=1
        return "Draw"
    elif (player == "Rock" and computer == "Scissors") or \
        (player == "Rock" and computer == "Lzard") or \
        (player == "Paper" and computer == "Rock") or \
        (player == "Paper" and computer == "Spock") or \
        (player == "Scissors" and computer == "Paper") or \
        (player == "Scissors" and computer == "Lizard") or \
        (player == "Spock" and computer == "Scissors") or \
        (player == "Spock" and computer == "Rock") or \
        (player == "Lizard" and computer == "Paper") or \
        (player == "Lizard" and computer == "Spock"):
        
        b_draw = False
        b_player_win = True
        b_computer_win = False
        player_wins = player_wins + 1
        return "Player Wins"
    else:
        b_draw = False
        b_computer_win = True
        b_player_win = False
        computer_wins += 1
        return "Computer Wins"


# Main game loop
def main():
    global computer_wins
    global player_wins
    global draw_num
    global b_player_win, b_computer_win, b_draw
    b_player_win = False
    b_computer_win = False
    b_draw = False
    running = True
    player_wins = 0
    computer_wins = 0
    draw_num = 0
    player_choice = None
    computer_choice = None
    result = None

    while running:
        screen.fill(BLACK)

        # Display choices
        screen.blit(game_img, (WIDTH-500, HEIGHT-500))
        # row 1
        screen.blit(rock_img, (80, 400))
        screen.blit(paper_img, (300, 400))
        screen.blit(scissors_img, (530, 400))
        # row 2
        screen.blit(spock_img, (80, 600))
        screen.blit(lizard_img, (300, 600))
        pygame.draw.rect(screen, DARK_GREY, (0, 0, WIDTH, 50))
        display_text("Menu", GREY, 20, 4)
        pygame.draw.rect(screen, GREY, (WIDTH / 2 - 180, 150, 150, 150))
        display_text("Ladder Level 2: Lizard Spock Guy", WHITE, WIDTH/2, 4)
        display_text('"Hey, I found this new way of playing!', WHITE, WIDTH/2, 150)
        display_text('Choose: Rock, Paper, Scissors, Lizard, Spock"', WHITE, WIDTH/2, 200)
        

        if b_player_win == True:
            display_text(f"{player_choice} beats {computer_choice}", GREEN, 50, 300)
            display_text(result, GREEN, 50, 350)
        if b_computer_win == True:
            display_text(f"{player_choice} losses to {computer_choice}", RED, 50, 300)
            display_text(result, RED, 50, 350)
        if b_draw == True:
            display_text(f"{player_choice} ties to {computer_choice}", BLUE, 50, 300)
            display_text(result, BLUE, 50, 350)

        if result:
            display_text(f"Player: {player_choice}", GREEN, 50, 200)
            display_text(f"Computer: {computer_choice}", RED, 450, 200)
            display_text(f"WINS: {player_wins}", GREEN, 50, 250)
            display_text(f"WINS: {computer_wins}", RED, 450, 250)
            display_text(f"DRAWS: {draw_num}", BLUE, 850, 250)
            
            
            

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
                elif 750 <= x <= 900 and 400 <= y <= 550:
                    player_choice = "Human"
                elif 950 <= x <= 1100 and 400 <= y <= 550:
                    player_choice = "Snake"
                elif 1150 <= x <= 1300 and 400 <= y <= 550:
                    player_choice = "Tree"
                elif 1350 <= x <= 1500 and 400 <= y <= 550:
                    player_choice = "Air"

                if player_choice:
                    computer_choice = random.choice(choices)
                    result = determine_winner(player_choice, computer_choice)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()