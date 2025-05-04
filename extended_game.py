import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions 800x600 
display_Width = 1920
display_Height = 1080
WIDTH, HEIGHT = display_Width, display_Height
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rock Paper Scissors")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Font
font = pygame.font.SysFont(None, 50)

# Choices
choices = ["Rock", "Paper", "Scissors", "Human", "Snake", "Tree", "Air", "Fire", "Water", "Lightning", "Gun", "Devil", "Dragon", "Wolf", "Sponge"]

# Load images
game_img = pygame.image.load("assets/help_extended_round.png")
rock_img = pygame.image.load("assets/card_rock.png")
paper_img = pygame.image.load("assets/card_paper.png")
scissors_img = pygame.image.load("assets/card_scissors.png")
human_img = pygame.image.load("assets/card_human.png")
snake_img = pygame.image.load("assets/card_snake.png")
tree_img = pygame.image.load("assets/card_tree.png")
air_img = pygame.image.load("assets/card_air.png")
fire_img = pygame.image.load("assets/card_fire.png")
water_img = pygame.image.load("assets/card_water.png")
lightning_img = pygame.image.load("assets/card_lightning.png")
gun_img = pygame.image.load("assets/card_gun.png")
devil_img = pygame.image.load("assets/card_devil.png")
dragon_img = pygame.image.load("assets/card_dragon.png")
wolf_img = pygame.image.load("assets/card_wolf.png")
sponge_img = pygame.image.load("assets/card_sponge.png")



# Scale images
game_img = pygame.transform.scale(game_img, (500, 500))
rock_img = pygame.transform.scale(rock_img, (150, 150))
paper_img = pygame.transform.scale(paper_img, (150, 150))
scissors_img = pygame.transform.scale(scissors_img, (150, 150))
human_img = pygame.transform.scale(human_img, (150, 150))
snake_img = pygame.transform.scale(snake_img, (150, 150))
tree_img = pygame.transform.scale(tree_img, (150, 150))
air_img = pygame.transform.scale(air_img, (150, 150))
fire_img = pygame.transform.scale(fire_img, (150, 150))
water_img = pygame.transform.scale(water_img, (150, 150))
lightning_img = pygame.transform.scale(lightning_img, (150, 150))
gun_img = pygame.transform.scale(gun_img, (150, 150))
devil_img = pygame.transform.scale(devil_img, (150, 150))
dragon_img = pygame.transform.scale(dragon_img, (150, 150))
wolf_img = pygame.transform.scale(wolf_img, (150, 150))
sponge_img = pygame.transform.scale(sponge_img, (150, 150))

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
        (player == "Rock" and computer == "Sponge") or \
        (player == "Rock" and computer == "Wolf") or \
        (player == "Rock" and computer == "Tree") or \
        (player == "Rock" and computer == "Human") or \
        (player == "Rock" and computer == "Snake") or \
        (player == "Rock" and computer == "Fire") or \
        (player == "Paper" and computer == "Rock") or \
        (player == "Paper" and computer == "Gun") or \
        (player == "Paper" and computer == "Lightning") or \
        (player == "Paper" and computer == "Devil") or \
        (player == "Paper" and computer == "Dragon") or \
        (player == "Paper" and computer == "Water") or \
        (player == "Paper" and computer == "Air") or \
        (player == "Scissors" and computer == "Paper") or \
        (player == "Scissors" and computer == "Air") or \
        (player == "Scissors" and computer == "Sponge") or \
        (player == "Scissors" and computer == "Wolf") or \
        (player == "Scissors" and computer == "Tree") or \
        (player == "Scissors" and computer == "Snake") or \
        (player == "Scissors" and computer == "Human") or \
        (player == "Gun" and computer == "Rock") or \
        (player == "Gun" and computer == "Fire") or \
        (player == "Gun" and computer == "Scissors") or \
        (player == "Gun" and computer == "Snake") or \
        (player == "Gun" and computer == "Human") or \
        (player == "Gun" and computer == "Tree") or \
        (player == "Gun" and computer == "Wolf") or \
        (player == "Fire" and computer == "Scissors") or \
        (player == "Fire" and computer == "Snake") or \
        (player == "Fire" and computer == "Human") or \
        (player == "Fire" and computer == "Tree") or \
        (player == "Fire" and computer == "Wolf") or \
        (player == "Fire" and computer == "Sponge") or \
        (player == "Fire" and computer == "Paper") or \
        (player == "Tree" and computer == "Paper") or \
        (player == "Tree" and computer == "Devil") or \
        (player == "Tree" and computer == "Dragon") or \
        (player == "Tree" and computer == "Water") or \
        (player == "Tree" and computer == "Air") or \
        (player == "Tree" and computer == "Paper") or \
        (player == "Tree" and computer == "Sponge") or \
        (player == "Tree" and computer == "Wolf") or \
        (player == "Human" and computer == "Wolf") or \
        (player == "Human" and computer == "Sponge") or \
        (player == "Human" and computer == "Paper") or \
        (player == "Human" and computer == "Air") or \
        (player == "Human" and computer == "Water") or \
        (player == "Human" and computer == "Dragon") or \
        (player == "Snake" and computer == "Water") or \
        (player == "Snake" and computer == "Air") or \
        (player == "Snake" and computer == "Paper") or \
        (player == "Snake" and computer == "Sponge") or \
        (player == "Snake" and computer == "Wolf") or \
        (player == "Snake" and computer == "Tree") or \
        (player == "Snake" and computer == "Human"):
        
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
        screen.blit(human_img, (730, 400))
        screen.blit(snake_img, (930, 400))
        screen.blit(tree_img, (1130, 400))
        screen.blit(air_img, (1330, 400))
        screen.blit(fire_img, (1530, 400))
        screen.blit(water_img, (1730, 400))
        # row 2
        screen.blit(lightning_img, (80, 600))
        screen.blit(gun_img, (300, 600))
        screen.blit(devil_img, (530, 600))
        screen.blit(dragon_img, (730, 600))
        screen.blit(wolf_img, (930, 600))
        screen.blit(sponge_img, (1130, 600))
        

        display_text("Extended game", WHITE, 150, 50)
        display_text("Choose: Rock, Paper, Scissors, Human, Snake", WHITE, 150, 90)
        display_text("Tree, Air, Fire, Water, Lightning, Gun, Devil, Dragon, Wolf, Sponge", WHITE, 150, 130)
        
        

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