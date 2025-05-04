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


story_mode_img = pygame.image.load('assets/round_story_mode_image.png').convert()
exodia_solitare_img = pygame.image.load('assets/round_exodia_solitare.png').convert()
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



def storymodeicon(x, y):
    small_img = pygame.transform.scale(story_mode_img, (200, 350))  # Resize the image to 100x100
    screen.blit(small_img, (x, y))
pass
def exodia_solitare_icon(x, y):
    small_img = pygame.transform.scale(exodia_solitare_img, (200, 350))  # Resize the image to 100x100
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

ROW_0_HEIGHT = 230
ROW_1_HEIGHT = 620

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
    dicerollerroundicon(340, 230)  # dice roller mode
    dicerollerroundicon(580, 230)
        
pass

def _page_2():
    '''Game type selection menu function'''
    
        
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
                if event.key == pygame.K_RIGHT:
                    print('Next page')
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