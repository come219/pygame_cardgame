import pygame
import random
import card

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
GREY = (128, 128, 128)
LIGHT_BLUE = (173, 216, 230)
LIGHT_GREEN = (144, 238, 144)
DARK_GREY = (69, 69, 69)

# Font
font = pygame.font.SysFont(None, 50)

# Choices
choices = ["Rock", "Paper", "Scissors", "Rock", "Paper", "Scissors"]

# Load images
deck_image = pygame.image.load("assets/deck_image.png")
graveyard_image = pygame.image.load("assets/graveyard_image.png")
rock_img = pygame.image.load("assets/card_rock.png")
paper_img = pygame.image.load("assets/card_paper.png")
scissors_img = pygame.image.load("assets/card_scissors.png")
card_back_image = pygame.image.load("assets/card_back.png")
card_info_image = pygame.image.load("assets/card_info.png")

# Scale images
rock_img = pygame.transform.scale(rock_img, (150, 150))
paper_img = pygame.transform.scale(paper_img, (150, 150))
scissors_img = pygame.transform.scale(scissors_img, (150, 150))
deck_img = pygame.transform.scale(deck_image, (150, 150))
graveyard_img = pygame.transform.scale(graveyard_image, (150, 150))
card_back_img = pygame.transform.scale(card_back_image, (150, 150))
card_info_img = pygame.transform.scale(card_info_image, (300, 400))


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




hand = []
draw_at_start = 5
b_drawn_start = False

card_rock = card.card("Rock", rock_img, 0, 0)

def show_hand_of_cards():
    b_drawn_start = False
    if b_drawn_start == False:
        if(len(hand) < draw_at_start):
            for i in range(draw_at_start):
                card = random.choice(choices)
                hand.append(card)
                card_rock.position(650 + i * 200, 850)

        
    screen.blit(card_back_img, (1600, 800))
    
    for i, card in enumerate(hand):
        if card == "Rock":
            screen.blit(card_rock.image, (card_rock.x, card_rock.y))
            # screen.blit(rock_img, (650 + i * 200, 850))
        elif card == "Paper":
            screen.blit(paper_img, (650 + i * 200, 850))
        elif card == "Scissors":
            screen.blit(scissors_img, (650 + i * 200, 850))
    b_drawn_start = True



def show_enemy_field():
    screen.blit(scissors_img, (1050, 390))
    screen.blit(scissors_img, (850, 390)) 



player_field = []    
def show_player_field():

    if len(player_field) != 0:
        

        screen.blit(rock_img, (850, 600))
        

    
    screen.blit(scissors_img, (1050, 600))


# Main game loop
def main():
    running = True
    player_choice = None
    computer_choice = None
    result = None

    held_card_in_field = False

    while running:
        screen.fill(BLACK)
        
        # Game UI

        display_text(f"History Log", BLUE, 50, 900)
        display_text(f"Player Health: 100", RED, 50, 1000)
        display_text(f"Graveyard: 0", LIGHT_BLUE, 1600, 540)
        screen.blit(graveyard_img, (1600, 590))
        display_text(f"Deck: 20", LIGHT_BLUE, 1600, 750)
        screen.blit(deck_img, (1600, 800))
        
        display_text(f"Enemy Health: 100", RED, 50, 100)
        display_text(f"Enemy Graveyard: 0", LIGHT_BLUE, 50, 360)
        screen.blit(graveyard_img, (50, 400))
        display_text(f"Enemy Deck: 20", LIGHT_BLUE, 50, 160)
        screen.blit(deck_img, (50, 200))

        display_text("Choose: Rock, Paper, or Scissors", BLACK, 150, 50)

        # Draw a grey rectangle menu bar at the top
        pygame.draw.rect(screen, DARK_GREY, (0, 0, WIDTH, 50))

        display_text(f"One Round Game", GREY, 860, 4)
        display_text(f"Menu", GREY, 50, 4)    # U+2302





        # enemy hand of cards
        screen.blit(card_back_img, (650, 150))
        screen.blit(card_back_img, (850, 150))
        screen.blit(card_back_img, (1050, 150))


        

        # playing field
        pygame.draw.rect(screen, GREY, (WIDTH / 2 - 350, HEIGHT/2 - 180, 800, 420))
        if held_card_in_field == True:
            pygame.draw.rect(screen, GREEN, (WIDTH / 2 - 350, HEIGHT/2 - 180, 800, 420))

        pygame.draw.rect(screen, BLACK, (WIDTH / 2 - 330, HEIGHT/2 - 160, 750, 380))

        
        show_player_field()
        show_enemy_field()

        show_hand_of_cards()

        screen.blit(card_info_img, (1600, 100))  #card info

        
        if False:
            display_text(f"End turn", BLUE, 1650, 1000)
        elif True:
            display_text(f"Draw", BLUE, 1650, 1000)
            
        




        if result:
            display_text(f"Player: {player_choice}", BLUE, 50, 200)
            display_text(f"Computer: {computer_choice}", RED, 50, 250)
            display_text(result, GREEN, 50, 300)

        for event in pygame.event.get():
            card_rock.handle_event(event)
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    import cardgame  # Import the cardgame module
                    cardgame.main()
                if event.key == pygame.K_d:
                    screen.blit(card_back_img, (1600, 800))

            elif event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                if WIDTH / 2 - 350 <= x <= WIDTH / 2 + 450 and HEIGHT / 2 - 180 <= y <= HEIGHT / 2 + 240:
                    held_card_in_field = True
                else:
                    held_card_in_field = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                # (650 + i * 200, 850)
                if 650 <= x <= 800 and 850 <= y <= 1000:
                    player_choice = "Rock"

                elif 850 <= x <= 1000 and 850 <= y <= 1000:
                    player_choice = "Paper"
                elif 1050 <= x <= 1200 and 850 <= y <= 1000:
                    player_choice = "Scissors"
                
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