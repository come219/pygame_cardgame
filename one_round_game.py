# pygame - card game, yugioh imitation
import pygame
import random
import card
from deck import Deck
from graveyard import Graveyard
from Banished import Banished
from enemy_deck import Enemy_Deck
from enemy_graveyard import Enemy_Graveyard
from enemy_banished import Enemy_Banished

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
LIGHT_RED = (255, 182, 193)
LIGHT_GREEN = (144, 238, 144)
DARK_GREY = (69, 69, 69)

# Font
font = pygame.font.SysFont(None, 50)
font_small = pygame.font.SysFont(None, 22)

# Load images
deck_image = pygame.image.load("assets/deck_image.png")
graveyard_image = pygame.image.load("assets/graveyard_image.png")
banished_image = pygame.image.load("assets/banished_icon.png")
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
banished_img = pygame.transform.scale(banished_image, (150, 150))
card_back_img = pygame.transform.scale(card_back_image, (150, 150))
card_info_img = pygame.transform.scale(card_info_image, (300, 400))
card_images = {
    "Rock": rock_img,
    "Paper": paper_img,
    "Scissors": scissors_img
}

draw_at_start = 5
global b_drawn_start
b_drawn_start = False
# player's hand, field, deck, graveyard, banished
hand = []
player_field = []   
player_deck = ["Rock", "Paper", "Scissors", "Scissors", "Rock",  "Paper",  ] 
player_graveyard = []
player_banished= []
deck_pos = (1700, 800)
graveyard_pos = (1750, 590)
banished_pos = (1600, 590)
deck = Deck(player_deck, card_images, deck_image, deck_pos)
graveyard = Graveyard(player_graveyard, card_images, graveyard_image, graveyard_pos )
banished = Banished(player_banished, card_images, banished_img, banished_pos)
# Choices - enemy deck
choices = ["Rock", "Paper", "Scissors", "Rock", "Paper", "Scissors"]
enemy_field = []
enemy_deck = ["Rock", "Paper", "Scissors", "Rock", "Paper", "Scissors"]
enemy_graveyard = []
enemy_banished = []
enemy_deck_pos = (50, 80)
enemy_graveyard_pos = (50, 300)
enemy_banished_pos = (250, 300)
enemy_deck = Enemy_Deck(enemy_deck, card_images, deck_image, enemy_deck_pos)
enemy_graveyard = Enemy_Graveyard(enemy_graveyard, card_images, graveyard_image, enemy_graveyard_pos)
enemy_banished = Enemy_Banished(enemy_banished, card_images, banished_image, enemy_banished_pos)


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



card_rock = card.card("Rock", rock_img, 0, 0)
card_paper = card.card("Paper", paper_img, 0, 0)
card_scissors = card.card("Scissorss", scissors_img, 0, 0)
card_back = card.card("Card", card_back_img, 1600, 800)
card_hand_1 = card.card("Card", paper_img, 0, 0)

card_objs = []

def check_card_clicked(mouse_pos ):
    if card_rock.is_clicked(card_rock, mouse_pos):
        return True


def show_hand_of_cards():
    global b_drawn_start, card_objs

    if not b_drawn_start:
        if len(hand) < draw_at_start:
            for i in range(draw_at_start):
                card_type = random.choice(player_deck)  # Draw a card from the player's deck
                player_deck.remove(card_type)
                hand.append(card_type)

                # Create a new card object for each card in the hand
                if card_type == "Rock":
                    card_obj = card.card("Rock", rock_img, 450 + i * 200, 850)
                elif card_type == "Paper":
                    card_obj = card.card("Paper", paper_img, 450 + i * 200, 850)
                elif card_type == "Scissors":
                    card_obj = card.card("Scissors", scissors_img, 450 + i * 200, 850)

                card_objs.append(card_obj)

    # Draw each card in the hand
    for card_obj in card_objs:
        card_obj.draw(screen)

    b_drawn_start = True

def show_hand_of_cards_old():
    global b_drawn_start
    
    if b_drawn_start == False:
        if(len(hand) < draw_at_start):
            for i in range(draw_at_start):
                # card = player_deck[i]
                card = random.choice(player_deck)    # should be player's deck
                player_deck.remove(card)
                hand.append(card)
                card_objs.append( card_rock )
                
        
    # screen.blit(card_back_img, (1600, 800))
    
    for i, card in enumerate(hand):
        if card == "Rock":
            
            # card_rock.position(650 + i * 200, 850)
            screen.blit(card_rock.image, (card_rock.x, card_rock.y))
            # screen.blit(card_back.image, (card_back.x, card_back.y))
            #card_back.flip_card(rock_img, screen )
            #card_back.moveto(650 + i * 200, 850, screen, 400)
            #card_back.position(650 + i * 200, 850)
            # screen.blit(rock_img, (650 + i * 200, 850))
        elif card == "Paper":
            screen.blit(card_paper.image, (card_paper.x, card_paper.y))
        elif card == "Scissors":
            screen.blit(card_scissors.image, (card_scissors.x, card_scissors.y))
            # screen.blit(scissors_img, (650 + i * 200, 850))
    
    if b_drawn_start == False:
        for i in range(len(hand)):
            if i == 0: 
                card_rock.x = 450 + i * 200
                card_rock.y = 850
            if i == 1:
                card_paper.x = 650 + i * 200
                card_paper.y = 850
                pass
            if i == 2:
                card_scissors.x = 850 + i * 200
                card_scissors.y = 850
    b_drawn_start = True


enemy_card_back = card.card("Card", card_back_img, 1050, 390)
enemy_card_back2 = card.card("Card", card_back_img, 850, 390)
def show_enemy_field():
    screen.blit(enemy_card_back.image, (1050, 390))

    screen.blit(enemy_card_back2.image, (850, 390)) 

def get_img(string):
    if string == "Rock":
        return rock_img
    if string == "Paper":
        return paper_img
    if string == "Scissors":
        return scissors_img
    
def reset_player_field():
    global player_field
    global list_player_choice
    player_field = []
    list_player_choice = []
    


def show_player_field():

    if len(player_field) != 0:
        screen.blit(get_img(player_field[0]), (850, 600))
        if len(player_field) >= 2:
            screen.blit(get_img(player_field[1]), (1050, 600))


global b_show_history_log 
b_show_history_log = False

def show_history_log():    
    if b_show_history_log == True:
        pygame.draw.rect(screen, DARK_GREY, ( WIDTH/4, HEIGHT/3.5, WIDTH /1.8, HEIGHT / 2))
        display_text(f"History Log", GREY, WIDTH / 2 - 50, HEIGHT / 3)
        display_text(f"0. Round 1 Start", GREY, WIDTH / 3 - 50, HEIGHT / 2.8)
        display_text(f"1. Player 1 Draws 5 Cards", GREY, WIDTH / 3 - 50, HEIGHT / 2.6)
        display_text(f"2. Player 2 Draws 5 Cards", GREY, WIDTH / 3 - 50, HEIGHT / 2.4)
        display_text(f"3. Player 2 Ends their turn", GREY, WIDTH / 3 - 50, HEIGHT / 2.2)



global b_show_graveyard 
b_show_graveyard = False
def show_player_graveyard():    
    if b_show_graveyard == True:
        pygame.draw.rect(screen, DARK_GREY, ( WIDTH/4, HEIGHT/3.5, WIDTH /1.8, HEIGHT / 2))
        display_text(f"Player Graveyard", BLUE, WIDTH / 2 - 50, HEIGHT / 3)
        display_text(f"Empty Card", GREY, WIDTH / 3 - 50, HEIGHT / 2.8)
        display_text(f"Empty Card", GREY, WIDTH / 3 - 50, HEIGHT / 2.6)
        display_text(f"Empty Card", GREY, WIDTH / 3 - 50, HEIGHT / 2.4)
        display_text(f"Empty Card", GREY, WIDTH / 3 - 50, HEIGHT / 2.2)


global b_show_banished 
b_show_banished = False
def show_player_banished():    
    if b_show_banished == True:
        pygame.draw.rect(screen, DARK_GREY, ( WIDTH/4, HEIGHT/3.5, WIDTH /1.8, HEIGHT / 2))
        display_text(f"Player Banished", BLUE, WIDTH / 2 - 50, HEIGHT / 3)
        display_text(f"Empty Card", GREY, WIDTH / 3 - 50, HEIGHT / 2.8)
        display_text(f"Empty Card", GREY, WIDTH / 3 - 50, HEIGHT / 2.6)
        display_text(f"Empty Card", GREY, WIDTH / 3 - 50, HEIGHT / 2.4)
        display_text(f"Empty Card", GREY, WIDTH / 3 - 50, HEIGHT / 2.2)


global b_is_end_turn
b_is_end_turn = True

clock = pygame.time.Clock()

# For double-click detection
DOUBLE_CLICK_TIME = 400  # milliseconds
last_click_time = 0


# Main game loop
def main():
    global player_field
    global list_player_choice

    global b_show_history_log, b_show_banished, b_show_graveyard, b_is_end_turn, result, last_click_time
    b_show_history_log = False
    b_show_graveyard = False
    b_show_banished = False
    running = True
    list_player_choice = []
    player_choice = None
    player_select_choice = None
    computer_choice = None
    result = None
    held_card_in_field = False





    def end_turn():
        global result
        computer_choice = random.choice(choices)
        computer_choice2 = random.choice(choices)

        # computer card flips
        if computer_choice == 'Rock':
            enemy_card_back.flip_card(card_rock.image, screen)
        if computer_choice2 == 'Rock':
            enemy_card_back2.flip_card(card_rock.image, screen)
        if computer_choice == 'Paper':
            enemy_card_back.flip_card(card_paper.image, screen)
        if computer_choice2 == 'Paper':
            enemy_card_back2.flip_card(card_paper.image, screen)
        if computer_choice == 'Scissors':
            enemy_card_back.flip_card(card_scissors.image, screen)
        if computer_choice2 == 'Scissors':
            enemy_card_back2.flip_card(card_scissors.image, screen)



        result = 'Undetermined'
        result01 = 'False'
        result02 = 'False'
        result03 = 'False'
        result04 = 'False'
        result1 = 'False'
        result2 = 'False'
        result3 = 'False'

        if len(player_field) == 0:
            result = 'Computer Wins'

        if len(player_field) != 0:
            result0 = determine_winner(player_field[0], computer_choice)
            result1 = determine_winner(player_field[0], computer_choice2)
            
            result2 = determine_winner(player_field[1], computer_choice2)
            result3 = determine_winner(player_field[1], computer_choice)

        if result == 'Player Wins' and result1 == 'Player Wins':
            result01 = 'Player Wins'
        elif result2 == 'Player Wins' and result3 == 'Player Wins':
            result02 = 'Player Wins'

        if result01 == 'Player Wins' and result02 == 'Player Wins':
            result = 'Player Wins'

        if result == 'Draw' and result1 == 'Draw':
            result01 = 'Draw'
        elif result2 == 'Draw' and result3 == 'Draw':
            result02 = 'Draw'
        
        if result == 'Player Wins' and result1 == 'Computer Wins':
            result01 = 'Player Wins 1'
        if result1 == 'Player Wins' and result == 'Computer Wins':
            result02 = 'Player Wins 2'
        if result2 == 'Player Wins' and result3 == 'Computer Wins':
            result03 = 'Player Wins 3'
        if result3 == 'Player Wins' and result2 == 'Computer Wins':
            result04 = 'Player Wins 4'
        

        # Determine the final result based on all outcomes
        if result01 == 'Player Wins' or result02 == 'Player Wins' or result03 == 'Player Wins' or result04 == 'Player Wins':
            result = 'Player Wins'
        elif result01 == 'Draw' or result02 == 'Draw':
            result = 'Draw'
        elif result01 == 'Computer Wins' or result02 == 'Computer Wins' or result03 == 'Computer Wins' or result04 == 'Computer Wins':
            result = 'Computer Wins'
        else:
            result = 'Undetermined'

        
        
        
        


    

    while running:
        screen.fill(BLACK)
        
        # Game UI
        
        
        display_text(f"Round: 1", GREY, 50, 850)
        display_text(f"History Log", BLUE, 50, 900)
        display_text(f"Player Health: 10", RED, 50, 1000)
        display_text(f"Player: {list_player_choice} {player_field} {player_choice}", BLUE, 50, 800)
        
        display_text(f"Enemy: {computer_choice}", RED, 50, 600)
        display_text(f"Enemy Health: 10", RED, 50, 500)
        num_player_deck = len(player_deck)
        display_text(f"result: {result}", GREEN, 50, 700)
        if result:
            display_text(result, GREEN, 450, 700)

        # Inside game loop
        deck.draw_deck_image(screen, font_small, text_color=LIGHT_BLUE)
        graveyard.draw_image(screen, font_small, text_color=LIGHT_BLUE)
        banished.draw_image(screen, font_small, text_color=LIGHT_BLUE)
        enemy_deck.draw_deck_image(screen, font_small, text_color=LIGHT_RED)
        enemy_graveyard.draw_image(screen, font_small, text_color=LIGHT_RED)
        enemy_banished.draw_image(screen, font_small, text_color=LIGHT_RED)

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

        screen.blit(card_info_img, (1550, 100))  #card info
        
        show_player_field()
        show_enemy_field()
        show_hand_of_cards()
        show_player_graveyard()
        show_player_banished()
        show_history_log()

        

        
        if b_is_end_turn == True:
            display_text(f"End turn", BLUE, 1650, 1000)
        elif True:
            display_text(f"Draw Cards", BLUE, 1650, 1000)
            
    
        
            

        for event in pygame.event.get():
            card_rock.handle_event(event)
            card_paper.handle_event(event)
            card_scissors.handle_event(event)
            if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
                # Pass the event to each card in the hand
                for card_obj in card_objs:
                    card_obj.handle_event(event)

            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    import cardgame  # Import the cardgame module
                    cardgame.main()
                if event.key == pygame.K_d:
                    screen.blit(card_back_img, (1600, 800))
                if event.key == pygame.K_h:
                    b_show_history_log = not b_show_history_log
                if event.key == pygame.K_g:
                    b_show_graveyard = not b_show_graveyard 
                if event.key == pygame.K_b:
                    b_show_banished = not b_show_banished
                if event.key == pygame.K_r:
                    reset_player_field()
                if event.key == pygame.K_e: # and enter?
                    b_is_end_turn = not b_is_end_turn
                    end_turn()

            elif event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                if WIDTH / 2 - 350 <= x <= WIDTH / 2 + 450 and HEIGHT / 2 - 180 <= y <= HEIGHT / 2 + 240:
                    held_card_in_field = True
                else:
                    held_card_in_field = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                current_time = pygame.time.get_ticks()
                if card_rock.x <= x <= card_rock.x + 100 and card_rock.y <= y <= card_rock.y +100:
                    player_choice = "Rock"
                if card_paper.x <= x <= card_paper.x + 100 and card_paper.y <= y <= card_paper.y +100:
                    player_choice = "Paper"
                if card_scissors.x <= x <= card_scissors.x + 100 and card_scissors.y <= y <= card_scissors.y +100:
                    player_choice = "Scissors"

                if current_time - last_click_time <= DOUBLE_CLICK_TIME:
                    print("Double Click Detected!")
                    # double tap to add (650 + i * 200, 850)
                    if card_rock.x <= x <= card_rock.x + 100 and card_rock.y <= y <= card_rock.y +100:
                        player_choice = "Rock"
                        list_player_choice.append("Rock")
                        player_field.append("Rock")
                    elif 850 <= x <= 1000 and 850 <= y <= 1000:
                        player_choice = "Paper"
                        list_player_choice.append("Paper")
                        player_field.append("Paper")
                    elif 1050 <= x <= 1200 and 850 <= y <= 1000:
                        player_choice = "Scissors"
                        list_player_choice.append("Scissors")
                        player_field.append("Scissors")
                    if 100 <= x <= 250 and 400 <= y <= 550:
                        player_choice = "Rock"
                    elif 325 <= x <= 475 and 400 <= y <= 550:
                        player_choice = "Paper"
                    elif 550 <= x <= 700 and 400 <= y <= 550:
                        player_choice = "Scissors"
                    

                last_click_time = current_time

            if event.type == pygame.MOUSEBUTTONUP:
                x, y = event.pos
                if player_choice == "Rock":
                    if WIDTH / 2 - 350 <= x <= WIDTH / 2 + 450 and HEIGHT / 2 - 180 <= y <= HEIGHT / 2 + 240:
                        player_field.append("Rock")
                        hand.remove("Rock")
                if player_choice == "Scissors":
                    if WIDTH / 2 - 350 <= x <= WIDTH / 2 + 450 and HEIGHT / 2 - 180 <= y <= HEIGHT / 2 + 240:
                        player_field.append("Scissors")
                        hand.remove("Scissors")
                if player_choice == "Paper":
                    if WIDTH / 2 - 350 <= x <= WIDTH / 2 + 450 and HEIGHT / 2 - 180 <= y <= HEIGHT / 2 + 240:
                        player_field.append("Paper")
                        hand.remove("Paper")
                


        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
