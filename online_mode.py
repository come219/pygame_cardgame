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
GREY = (128, 128, 128)
DARK_GREY = (69, 69, 69)
LIGHT_GREY = (211, 211, 211)


# Font
font = pygame.font.SysFont(None, 50)


oneroundImg = pygame.image.load('assets/one_round_image.png').convert()
traditionalroundImg = pygame.image.load('assets/traditional_round_image.png').convert()
classic_roundImg = pygame.image.load('assets/classic_game_image.png').convert()
extended_roundImg = pygame.image.load('assets/extended_round_image.png').convert()
online_roundImg = pygame.image.load('assets/online_game_image.png').convert()
dice_roller_Img = pygame.image.load('assets/dice_roller_image.png').convert()
spock_roundImg = pygame.image.load('assets/spock_round_image.png').convert()


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


def onlineroundicon(x, y):
    smaller_oneroundImg = pygame.transform.scale(online_roundImg, (200, 350))
    screen.blit(smaller_oneroundImg, (x, y))
pass


def extendedroundicon(x, y):
    smaller_oneroundImg = pygame.transform.scale(extended_roundImg, (200, 350))
    screen.blit(smaller_oneroundImg, (x, y))
pass


def dicerollerroundicon(x, y):
    smaller_oneroundImg = pygame.transform.scale(dice_roller_Img, (200, 350))
    screen.blit(smaller_oneroundImg, (x, y))
pass

def spockroundicon(x, y):
    smaller_oneroundImg = pygame.transform.scale(spock_roundImg, (200, 350))
    screen.blit(smaller_oneroundImg, (x, y))
pass


ROW_0_HEIGHT = 230
ROW_1_HEIGHT = 620

def _page_0():
    '''Game type selection menu function'''
    # row 1
    oneroundicon(120, ROW_0_HEIGHT)           # one round mode
    traditionalroundicon(340, ROW_0_HEIGHT)  # traditional mode
    extendedroundicon(580, ROW_0_HEIGHT)     # online mode
    onlineroundicon (840, ROW_0_HEIGHT)     # online mode
    classicroundicon(1080, ROW_0_HEIGHT)      # classic modes -> best of 3
    spockroundicon(1340, ROW_0_HEIGHT)        # spock lizard mode
    # row 2
    dicerollerroundicon(120, ROW_1_HEIGHT)  # dice roller mode
    dicerollerroundicon(340, ROW_1_HEIGHT)  # dice roller mode
    dicerollerroundicon(580, ROW_1_HEIGHT)  # dice roller mode
    dicerollerroundicon(840, ROW_1_HEIGHT)  # dice roller mode
    dicerollerroundicon(1080, ROW_1_HEIGHT)  # dice roller mode
    dicerollerroundicon(1340, ROW_1_HEIGHT)  # dice roller mode


def _page_1():
    '''Game type selection menu function'''
    classicroundicon(100, 230)      # classic modes -> best of 3
    spockroundicon(600, 230)        # spock lizard mode
    dicerollerroundicon(1100, 230)  # dice roller mode
    
        
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
    b_create_server = False
    b_join_server = True
    b_in_lobby = False
    b_is_locked_in = False

    global CURRENT_PAGE
    while running:
        
        screen.fill(BLACK)
        pygame.draw.rect(screen, DARK_GREY, (0, 0, WIDTH, 50))
        pygame.draw.rect(screen, DARK_GREY, (80, 210, WIDTH - 400, HEIGHT - 300))
        
        
        

        if b_join_server:
            display_text(f"Online Mode - Join Server", BLUE, 860, 4)
        elif b_create_server:
            pygame.draw.rect(screen, LIGHT_GREY, (300, HEIGHT - 580, 1200, 490))
            display_text(f"Online Mode - Create Server", BLUE, 860, 4)
            display_text(f"Player 1: (Player)", RED, 460, 450)
            display_text(f"Player 2: _", BLUE, 1060, 450)
            display_text(f"00:00 | (Player) created Server at IP: 0.0.0.0", BLACK, 380, 550)
            display_text(f"00:00 | lobby id: classic_1234", BLACK, 380, 600)
        elif b_in_lobby:
            pygame.draw.rect(screen, LIGHT_GREY, (300, HEIGHT - 580, 1200, 490))
            display_text(f"Online Mode - In Lobby", RED, 860, 4)
            display_text(f"Player 1: (Host)", RED, 460, 450)
            display_text(f"Player 2: (Player)", BLUE, 1060, 450)
            display_text(f"00:00 | (Player) joined Server at IP: 0.0.0.0", BLACK, 380, 550)
            display_text(f"00:00 | lobby id: classic_1234", BLACK, 380, 600)
            

        display_text(f"Server Name", GREY, 100, 250)
        display_text(f"Host Name", GREY, 400, 250)
        display_text(f"Gamemode", GREY, 700, 250)
        display_text(f"Players", GREY, 1000, 250)
        display_text(f"Status", GREY, 1250, 250)
        display_text(f"Ping", GREY, 1450, 250)

        display_text(f"Refresh", BLUE, 1660, 250)

        if b_join_server == True:
            display_text(f"Create Server", BLUE, 1660, 450)
            display_text(f"Enter IP", BLUE, 1660, 600)
            display_text(f"Lobby ID", BLUE, 1660, 700)
            display_text(f"Join Server", BLUE, 1660, 850)
        elif b_in_lobby == True:
            if b_is_locked_in == True:
                display_text(f"Lock In", BLUE, 1660, 450)   
            elif b_is_locked_in == False:
                display_text(f"Unlock", GREY, 1660, 450)
            display_text(f"Leave Server", BLUE, 1660, 650)
            display_text(f"Waiting for", GREY, 1660, 850)
            display_text(f"Game to start", GREY, 1660, 900)
        elif b_create_server: 
            if b_is_locked_in == True:
                display_text(f"Lock In", RED, 1660, 450)   
            elif b_is_locked_in == False:
                display_text(f"Unlock", BLUE, 1660, 450)
            display_text(f"Leave Server", RED, 1660, 650)
            if True:
                display_text(f"Start Game", GREY, 1660, 850)
            elif True:
                display_text(f"Start Game", GREEN, 1660, 850)
            

        pygame.draw.rect(screen, LIGHT_GREY, ((WIDTH/2 - 200), 80, 80, 80))   
        display_text(f"Player", BLUE, (WIDTH / 2) - 100, 80)
        display_text(f"Balance :\$0.00", GREEN, (WIDTH / 2) - 100, 140)
        

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
                if event.key == pygame.K_r:
                    print('refreshing servers')
                if event.key == pygame.K_j:
                    print('joining server')
                    b_join_server = False
                    b_in_lobby = True
                if event.key == pygame.K_l:
                    print('leaving server')
                    b_join_server = True
                    b_create_server = False
                    b_in_lobby = False
                    b_is_locked_in = False
                if event.key == pygame.K_e:
                    print('Enter IP')
                if event.key == pygame.K_c:
                    print('creating server')
                    b_join_server = False
                    b_create_server = True
                if event.key == pygame.K_i:
                    print('locking/unlocking')
                    b_is_locked_in = not b_is_locked_in




        pygame.display.flip()
    pygame.quit()



if __name__ == "__main__":
    main()