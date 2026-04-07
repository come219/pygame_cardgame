import pygame
import os
import sys  
import cardgame


# Initialize Pygame
pygame.init()
# Screen dimensions 800x600 
display_Width = 1920
display_Height = 1080
WIDTH, HEIGHT = display_Width, display_Height
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Type Selection")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (173, 216, 230)
LIGHT_GREEN = (144, 238, 144)
DARK_GREY = (69, 69, 69)
LIGHT_GREY = (211, 211, 211)


# Font
font = pygame.font.SysFont(None, 50)


exodia_solitare_img = pygame.image.load('assets/round_exodia_solitare.png').convert()
blackjack_img = pygame.image.load('assets/round_blackjack.png').convert()
roulette_img = pygame.image.load('assets/round_roulette.png').convert()
snake_game_img = pygame.image.load('assets/round_snake.png').convert()
captains_mode_img = pygame.image.load('assets/round_captains_mode.png').convert()
auto_cs_img = pygame.image.load('assets/round_auto_cs_image.png').convert()
auto_cs_2_player_img = pygame.image.load('assets/round_auto_cs_2_player_image.png').convert()
coin_flip_img = pygame.image.load('assets/round_coin_flip.png').convert()
quantum_4d_coin_flip_img = pygame.image.load('assets/round_quantum_4d_coin_flip.png').convert()

story_mode_img = pygame.image.load('assets/round_story_mode_image.png').convert()
oneroundImg = pygame.image.load('assets/one_round_image.png').convert()
traditionalroundImg = pygame.image.load('assets/traditional_round_image.png').convert()
classic_roundImg = pygame.image.load('assets/classic_game_image.png').convert()
classic_2_player_roundImg = pygame.image.load('assets/classic_2_player_game_image.png').convert()
extended_roundImg = pygame.image.load('assets/extended_round_image.png').convert()
extended_round_2_player_Img = pygame.image.load('assets/extended_plus_2_player_image.png').convert()
online_roundImg = pygame.image.load('assets/online_game_image.png').convert()
test_roundImg = pygame.image.load('assets/round_test_image.png').convert()
dice_roller_Img = pygame.image.load('assets/dice_roller_image.png').convert()
spock_roundImg = pygame.image.load('assets/spock_round_image.png').convert()
spock_round_2_player_Img = pygame.image.load('assets/spock_2_player_round_image.png').convert()



gun_duel_img = pygame.image.load('assets/gun_duel_image.png').convert()
shoot_reload_repeat_img = pygame.image.load('assets/shoot_reload_repeat_image.png').convert()


def storymodeicon(x, y):
    small_img = pygame.transform.scale(story_mode_img, (200, 350))  # Resize the image to 100x100
    screen.blit(small_img, (x, y))
pass
def exodia_solitare_icon(x, y):
    small_img = pygame.transform.scale(exodia_solitare_img, (200, 350))  # Resize the image to 100x100
    screen.blit(small_img, (x, y))
pass
def blackjack_icon(x, y):
    small_img = pygame.transform.scale(blackjack_img, (200, 350))  # Resize the image to 100x100
    screen.blit(small_img, (x, y))
pass

def roulette_icon(x, y):
    small_img = pygame.transform.scale(roulette_img, (200, 350))  # Resize the image to 100x100
    screen.blit(small_img, (x, y))
pass
def snake_game_icon(x, y):
    small_img = pygame.transform.scale(snake_game_img, (200, 350))  # Resize the image to 100x100
    screen.blit(small_img, (x, y))
pass
def auto_cs_icon(x, y):
    small_img = pygame.transform.scale(auto_cs_img, (200, 350))  # Resize the image to 100x100
    screen.blit(small_img, (x, y))
pass
def auto_cs_2_player_icon(x, y):
    small_img = pygame.transform.scale(auto_cs_2_player_img, (200, 350))  # Resize the image to 100x100
    screen.blit(small_img, (x, y))
pass
def coin_flip_icon(x, y):
    small_img = pygame.transform.scale(coin_flip_img, (200, 350))  # Resize the image to 100x100
    screen.blit(small_img, (x, y))
pass
def quantum_4d_coin_flip_icon(x, y):
    small_img = pygame.transform.scale(quantum_4d_coin_flip_img, (200, 350))  # Resize the image to 100x100
    screen.blit(small_img, (x, y))
pass
def captains_mode_icon(x, y):
    small_img = pygame.transform.scale(captains_mode_img, (200, 350))  # Resize the image to 100x100
    screen.blit(small_img, (x, y))
pass
def oneroundicon(x, y):
    smaller_oneroundImg = pygame.transform.scale(oneroundImg, (200, 350))
    screen.blit(smaller_oneroundImg, (x, y))
pass
def traditionalroundicon(x, y):
    smaller_oneroundImg = pygame.transform.scale(traditionalroundImg, (200, 350))
    screen.blit(smaller_oneroundImg, (x, y))
pass

def classicroundicon(x, y):
    smaller_oneroundImg = pygame.transform.scale(classic_roundImg, (200, 350))
    screen.blit(smaller_oneroundImg, (x, y))
pass
def classic_2_player_roundicon(x, y):
    smaller_oneroundImg = pygame.transform.scale(classic_2_player_roundImg, (200, 350))
    screen.blit(smaller_oneroundImg, (x, y))
pass


def onlineroundicon(x, y):
    smaller_oneroundImg = pygame.transform.scale(online_roundImg, (200, 350))
    screen.blit(smaller_oneroundImg, (x, y))
pass


def test_roundicon(x, y):
    small_img = pygame.transform.scale(test_roundImg, (200, 350))
    screen.blit(small_img, (x, y))
pass


def extendedroundicon(x, y):
    smaller_oneroundImg = pygame.transform.scale(extended_roundImg, (200, 350))
    screen.blit(smaller_oneroundImg, (x, y))
pass


def extendedround_2_player_icon(x, y):
    smaller_roundImg = pygame.transform.scale(extended_round_2_player_Img, (200, 350))
    screen.blit(smaller_roundImg, (x, y))
pass


def dicerollerroundicon(x, y):
    smaller_oneroundImg = pygame.transform.scale(dice_roller_Img, (200, 350))
    screen.blit(smaller_oneroundImg, (x, y))
pass

def spockroundicon(x, y):
    smaller_oneroundImg = pygame.transform.scale(spock_roundImg, (200, 350))
    screen.blit(smaller_oneroundImg, (x, y))
pass
def spockround_2_playericon(x, y):
    smaller_roundImg = pygame.transform.scale(spock_round_2_player_Img, (200, 350))
    screen.blit(smaller_roundImg, (x, y))
pass

def gun_duel_icon(x, y):
    smaller_roundImg = pygame.transform.scale(gun_duel_img, (200, 350))
    screen.blit(smaller_roundImg, (x, y))
pass

def shoot_reload_repeat_icon(x, y): 
    smaller_roundImg = pygame.transform.scale(shoot_reload_repeat_img, (200, 350))
    screen.blit(smaller_roundImg, (x, y))
pass

ROW_0_HEIGHT = 230
ROW_1_HEIGHT = 620

def _page_minus_1():
    '''Game type selection menu function'''
    display_text("1 - Level 1: Best of 3 Rock paper Scissors Boy         | Reward:   $1 |", WHITE, WIDTH // 7, HEIGHT // 3)
    display_text("2 - Level 2: Best of 5 Lizard Spock Man                | Reward:   $3 | ", WHITE, WIDTH //7, HEIGHT // 3 + 50)
    display_text("3 - Level 3: 1 Round Extended Game Girl                | Reward:   $0 |", WHITE, WIDTH //7, HEIGHT // 3 + 100)
    display_text("4 - Level 4: One Round Game Boy                        | Reward:   $5 |", WHITE, WIDTH // 7, HEIGHT // 3 + 150)
    display_text("5 - Level 5: One Traditional Game Boy                  | Reward:  $10 |", WHITE, WIDTH // 7, HEIGHT // 3 + 200)
    display_text("6 - Level 6: 1 Heads or Tails Old Man                  | Reward:   $1 |", WHITE, WIDTH // 7, HEIGHT // 3 + 250)
    display_text("7 - Level 7: 1 Quantum 4D Heads or Tails Mad Scientist | Reward:   $2 |", WHITE, WIDTH // 7, HEIGHT // 3 + 300)
    display_text("8 - Level 8: US Roulette 10 Rounds Casino       | Potential Reward:  $100 |  Buy-in $10 |", WHITE, WIDTH // 7, HEIGHT // 3 + 350)
    display_text("9 - Level 9: EU Roulette 10 Rounds Casino       | Potential Reward:  $100 |  Buy-in $10 |", WHITE, WIDTH // 7, HEIGHT // 3 + 400)
    display_text("0 - Level 10: Blackjack, 10 Rounds Mafia Grunt  | Potential Reward: $1000 | Buy-in $100 |", WHITE, WIDTH // 7, HEIGHT // 3 + 450)
    display_text("? - Level 11: All-in Poker Mafia Kingpin        | Potential Reward: $???? | Buy-in $ All-in |", WHITE, WIDTH // 7, HEIGHT // 3 + 500)
    display_text("? - Level 12: Russian Roulette Mafia Kingpin    | Potential Reward: Your Life | Buy-in 1 Life   |", WHITE, WIDTH // 7, HEIGHT // 3 + 550)
    display_text("? - Level 99: Recieve a Random Card.            | Reward:$1000 + 1 Card |", WHITE, WIDTH // 7, HEIGHT // 3 + 600)

    display_text("Story Mode", WHITE, WIDTH // 2 - 100, HEIGHT // 5)
    display_text("Ladder List", WHITE, WIDTH // 2 - 100, HEIGHT // 4)

    pass


def _page_0():
    '''Game type selection menu function'''
    # row 1
    storymodeicon(120, ROW_0_HEIGHT)           # story mode
    oneroundicon(340, ROW_0_HEIGHT)  # one round mode
    traditionalroundicon(580, ROW_0_HEIGHT)     # traditional mode
    onlineroundicon (840, ROW_0_HEIGHT)     # online mode
    test_roundicon(1080, ROW_0_HEIGHT)      # 
    dicerollerroundicon(1340, ROW_0_HEIGHT)        # spock lizard mode
    # row 2
    classicroundicon(120, ROW_1_HEIGHT)  # 
    classic_2_player_roundicon(340, ROW_1_HEIGHT)  # 
    spockroundicon(580, ROW_1_HEIGHT)  # 
    spockround_2_playericon(840, ROW_1_HEIGHT)  #
    extendedroundicon(1080, ROW_1_HEIGHT)  #
    extendedround_2_player_icon(1340, ROW_1_HEIGHT)  #


def _page_1():
    '''Game type selection menu function'''
    exodia_solitare_icon(120, 230)      # classic modes -> best of 3
    blackjack_icon(340, 230)  # dice roller mode
    roulette_icon(580, 230)
    snake_game_icon(840, 230)
    auto_cs_icon(1080, ROW_0_HEIGHT)
    auto_cs_2_player_icon(1340, ROW_0_HEIGHT)
    # row 2
    captains_mode_icon(120, ROW_1_HEIGHT)
    coin_flip_icon(340, ROW_1_HEIGHT)
    quantum_4d_coin_flip_icon(580, ROW_1_HEIGHT)

        
pass

def _page_2():
    '''Game type selection menu function'''
    gun_duel_icon(120, 230)      # 
    shoot_reload_repeat_icon(340, 230)  # 
        
pass



# Function to display text
def display_text(text, color, x, y):
    screen_text = font.render(text, True, color)
    screen.blit(screen_text, (x, y))

        

CURRENT_PAGE = 0

# Main game loop
def main():
    running = True

    global CURRENT_PAGE
    while running:
        
        screen.fill(BLACK)
        # Draw a grey rectangle menu bar at the top
        pygame.draw.rect(screen, DARK_GREY, (0, 0, WIDTH, 50))
        pygame.draw.rect(screen, DARK_GREY, (80, 210, WIDTH - 400, HEIGHT - 300))
        
        if CURRENT_PAGE == -1:
            _page_minus_1()
        if CURRENT_PAGE == 0:
            _page_0()
        elif CURRENT_PAGE == 1:
            _page_1()
        elif CURRENT_PAGE == 2:
            _page_2()

        display_text(f"Game Mode - Game Type", BLUE, 860, 4)

        pygame.draw.rect(screen, LIGHT_GREY, ((WIDTH - 450), 80, 80, 80))    
        display_text(f"Player", BLUE, WIDTH - 350, 80)
        display_text(f"Balance :\$0.00", GREEN, WIDTH - 350, 140)
        pygame.draw.rect(screen, LIGHT_GREY, ((WIDTH/2 - 250), 80, 80, 80))   
        pygame.draw.rect(screen, LIGHT_GREY, ((WIDTH/2 + 150), 80, 80, 80))  
        display_text(f"Page {CURRENT_PAGE} / 20", BLUE, (WIDTH / 2) - 100, 80)
        display_text(f"<", BLUE, (WIDTH / 2 - 130) - 100, 80)
        display_text(f">", BLUE, (WIDTH / 2 + 270) - 100, 80)


        display_text(f"Menu", BLUE, 50, 4)


        # event check
        for event in pygame.event.get():
                            #print(event)
            if event.type == pygame.QUIT:
                print('QUIT: by execution!')
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:                                                 
                if event.key == pygame.K_ESCAPE:
                    print('Return to mainmenu!')
                    cardgame.main()  # Import the cardgame module
                if event.key == pygame.K_LEFT:
                    print('Previous page')
                    CURRENT_PAGE = CURRENT_PAGE - 1
                if event.key == pygame.K_RIGHT:
                    print('Next page')
                    CURRENT_PAGE = CURRENT_PAGE + 1
                if event.key == pygame.K_1:
                    print('Starting 1 round game')
                    import game  # Import the game module
                    game.main()
                if event.key == pygame.K_2:
                    print('Starting full game')
                    import rock_paper_scissors  # Import the game module
                    rock_paper_scissors.main()  # Call the start_full_game function from game.py
                if event.key == pygame.K_3:
                    print('Starting online menu')


        pygame.display.flip()
    pygame.quit()



if __name__ == "__main__":
    main()