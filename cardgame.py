#################################################
#################################################
####    Sebastian St Johnston - come219      ####
####    Untitled Card Game Version 0.02      ####
####                                         ####
####    Patch notes:                         ####
####    0.01: created gameloop, menus actv   ####
####    0.02: working deck of cards visually ####
####                                         ####
####                                         ####
####                                         ####
####                                         ####
####                                         ####
#################################################



##
#
#   INCLUDES for different apis, developments and libraries

##
#   pygame: Game Engine and Graphical display capabilities
##
from pygame_functions import *

import card_viewer






#   END OF INCLUDE
##





########################
##  DEFINED COLOURS   ##
########################


white = (255,255,255)
grey = (128,128,128)
black = (0,0,0)
red = (255,0,0)
salmon = (250,128,114)
pink = (255,20,147)
green = (100, 255, 100)
teal = (0, 128, 128)
newblue = (86,86,239)





##########################
#   Display parameters   #
##########################

#initalize pygame
pygame.init()

#display size constants
display_Width = 1920
display_Height = 1080
WIDTH = display_Width
HEIGHT = display_Height

#gameDisplay defined
#tuple paramater for screen display size
gameDisplay = pygame.display.set_mode((display_Width,display_Height))

#display title
pygame.display.set_caption('Card Game')

#define time
clock = pygame.time.Clock()

#font defintion
#font=x(a, fontsize)
font = pygame.font.SysFont(None, 25)
font2 = pygame.font.SysFont(None, 50)
font3 = pygame.font.SysFont(None, 70)

#################################
#   message-to-screen functions #
#################################
def message_to_screen(msg, color):
    screen_text = font.render(msg, True, color)
    gameDisplay.blit(screen_text, [100, 100])

pass

def message_to_screen2(msg, color, x, y):
    screen_text = font2.render(msg, True, color)
    gameDisplay.blit(screen_text, [x, y])

pass


def message_title(msg, color):
    screen_text = font3.render(msg, True, color)
    gameDisplay.blit(screen_text, [100, 100])

pass








#Loading in images into pygame variables
mainMenuBackgroundImg = pygame.image.load('assets/mainmenubackground.png').convert()
mainmenubarImg = pygame.image.load('assets/mainmenubar.png').convert()
logo_game_image = pygame.image.load('assets/logo_game_logo_512.png').convert()
logo_game_img = pygame.transform.scale(logo_game_image, (200, 200))
logo_game_img_small = pygame.transform.scale(logo_game_image, (80, 80))
logo_company_image = pygame.image.load('assets/logo_219studios_logo_512.png').convert()
logo_company_img = pygame.transform.scale(logo_company_image, (80, 80))
logo_company_img_small = pygame.transform.scale(logo_company_image, (80, 80))

# menu buttons
playgamebuttonImg = pygame.image.load("assets/button_play_game.png").convert()
changedeckbuttonImg = pygame.image.load("assets/button_change_deck.png").convert()
learnImg = pygame.image.load("assets/button_learn.png").convert()
settingsbuttonImg = pygame.image.load("assets/button_settings.png").convert()
x_buttonImg = pygame.image.load("assets/button_x.png").convert()
cancel_buttonImg = pygame.image.load("assets/button_cancel.png").convert()
cancel_buttonImg = pygame.transform.scale(cancel_buttonImg, (300, 120))
quitgamebuttonImg = pygame.image.load("assets/button_quit_game.png").convert()
quitgamebutton_scaled = pygame.transform.scale(quitgamebuttonImg, (300, 120))

x_button_scaled = pygame.transform.scale(x_buttonImg, (120, 80))
gobackbuttonImg = pygame.image.load("assets/button_go_back.png").convert()
gamemodesbuttonImg = pygame.image.load("assets/button_game_modes.png").convert()

changedeckbackgroundImg = pygame.image.load('assets/changedeckbackground.png').convert()
changedeckbackgroundImg2 = pygame.image.load('assets/changedeckbackgroundedit.png').convert()


story_mode_img = pygame.image.load('assets/round_story_mode_image.png').convert()
oneroundImg = pygame.image.load('assets/one_round_image.png').convert()
traditionalroundImg = pygame.image.load('assets/traditional_round_image.png').convert()
classic_roundImg = pygame.image.load('assets/classic_game_image.png').convert()
extended_roundImg = pygame.image.load('assets/extended_round_image.png').convert()
online_roundImg = pygame.image.load('assets/online_game_image.png').convert()
dice_roller_Img = pygame.image.load('assets/dice_roller_image.png').convert()
spock_roundImg = pygame.image.load('assets/spock_round_image.png').convert()


#with open('currentdeck.txt') as currentdeckData:
currentdeckData = open("currentdeck.txt")
currentdecktext = currentdeckData.read()


#cardgame_
sizeofdeck = currentdecktext[9:]

newdeck = open('newdeck.txt')

#currentdecktxt = currentdeck.read()
#newdecktxt = newdeck.read()


cardaImg = pygame.image.load('assets/card_rock.png').convert()
cardbImg = pygame.image.load('assets/card_paper.png').convert()
cardcImg = pygame.image.load('assets/card_scissors.png').convert()

cardaImg = pygame.transform.scale(cardaImg, (100, 150))
cardbImg = pygame.transform.scale(cardbImg, (100, 150))
cardcImg = pygame.transform.scale(cardcImg, (100, 150))


#####################################
#   draw image function             #
#####################################
def drawImage(pygameimage, x, y):
    gameDisplay.blit(pygameimage,(x,y))
pass




###################################
#   quitgamebutton function     #
###################################
def quitgamebutton(x, y):

    gameDisplay.blit(quitgamebuttonImg,(x, y))
    
pass


#####################################
#   mainMenuBackground function     #
#####################################
def changedeckbackground(x, y):

    

    if(editdeckchange) == True:
        gameDisplay.blit(changedeckbackgroundImg2,(x, y))
    else:
        gameDisplay.blit(changedeckbackgroundImg,(x, y))
    

pass

#####################################
#   mainMenuBackground function     #
#####################################
def storymodeicon(x, y):
    small_img = pygame.transform.scale(story_mode_img, (400, 600))  # Resize the image to 100x100
    gameDisplay.blit(small_img, (x, y))
pass
def oneroundicon(x, y):
    small_img = pygame.transform.scale(oneroundImg, (400, 600))  # Resize the image to 100x100
    gameDisplay.blit(small_img, (x, y))
pass
def traditionalroundicon(x, y):
    small_img = pygame.transform.scale(traditionalroundImg, (400, 600))  # Resize the image to 100x100
    gameDisplay.blit(small_img, (x, y))
pass

def classicroundicon(x, y):
    small_img = pygame.transform.scale(classic_roundImg, (400, 600))  # Resize the image to 100x100
    gameDisplay.blit(small_img, (x, y))
pass


def onlineroundicon(x, y):
    small_img = pygame.transform.scale(online_roundImg, (400, 600))  # Resize the image to 100x100
    gameDisplay.blit(small_img, (x, y))
pass


def extendedroundicon(x, y):
    small_img = pygame.transform.scale(extended_roundImg, (400, 600))  # Resize the image to 100x100
    gameDisplay.blit(small_img, (x, y))
pass


def dicerollerroundicon(x, y):
    small_img = pygame.transform.scale(dice_roller_Img, (400, 600))  # Resize the image to 100x100
    gameDisplay.blit(small_img, (x, y))
pass

def spockroundicon(x, y):
    small_img = pygame.transform.scale(spock_roundImg, (400, 600))  # Resize the image to 100x100
    gameDisplay.blit(small_img, (x, y))
pass




#########################
#   drawCards function  #
#########################


#deck area coordinates
changedeckcardpos = [(100,100), (250,100), (400,100), (550,100),(700,100), (850,100), (1000,100), (1150,100),
                     (100,300), (250,300), (400,300), (550,300),(700,300), (850,300), (1000,300), (1150,300)]

#collection area coordinates
collectioncardpos =  [(100,800), (250,800), (400,800), (550,800),(700,800), (850,800), (1000,800), (1150,800)]


def drawCards(card, cardpos):

    if(card == 'a'):
        
        gameDisplay.blit(cardaImg, cardpos)
        
    elif(card == 'b'):
        
        gameDisplay.blit(cardbImg, cardpos)
        
    elif(card == 'c'):
        
        gameDisplay.blit(cardcImg, cardpos)



pass






##############################################################################################################################################
##############################################################################################################################################

##                                              GAME MENU CYCLE FUNCTIONS                                                                  ##

##############################################################################################################################################
##############################################################################################################################################



#########################
#   gameLoop function   #
#########################
def gameLoop():


    #print('gameLoop')

    #gameLoop parameters
    #gameRunning = True



##    #!main loop
##    while gameRunning:
##
##
##            #!event check
##            for event in pygame.event.get():
##                
##                #print(event)
##
##               if event.type == pygame.QUIT:
##                   #gameRunning = False
##                   isRunning = False
##                  
##                   
##               if event.type == pygame.KEYDOWN:
##            
##                    if event.key == pygame.K_q:
##                        #gameRunning = False
##                        isRunning = False
##                    if event.key == pygame.K_ESCAPE:
##                        #gameRunning = False
##                        isRunning = False
                        


            #!gameLoop instanced functions
            #gameBackground fill
            gameDisplay.fill(white)
            


        
pass







#############################
#   changeDeck function     #
#############################

#changedeck function boolean menu variables
editdeckchange = False
noteditingdeckchange = False
clearselectdeckchange = False

olddeck = []





def changeDeckMenu():
    '''Change deck menu function'''
    #print('changedeckmenu')
    global gameMenu
    global sizeofdeck
    global editdeckchange
    global noteditingdeckchange
    global clearselectdeckchange

    #print(olddeck)

    
    
    #!event check
    for event in pygame.event.get():
                        #print(event)
        if event.type == pygame.QUIT:
            print('QUIT: by execution!')
            quitgame()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if(editdeckchange) == True:
                pos = pygame.mouse.get_pos()
                print(pos)

        elif event.type == pygame.KEYDOWN:
            #If actively editing
            if(editdeckchange) == True:
                if event.key == pygame.K_s:
                    
                    noteditingdeckchange = True
                    editdeckchange = False
                    clearselectdeckchange = False
                    #save new edit
                    #write sizeofdeck to the text file
                    print('saved selection!')
                    

                if event.key == pygame.K_c:
                    noteditingdeckchange = False
                    clearselectdeckchange = True
                    sizeofdeck = ""
                    #move the deck to 
                    print('clear selection')

                if event.key == pygame.K_z:
                    noteditingdeckchange = False
                    clearselectdeckchange = False
                    editdeckchange = False


                    #undo previous action    --> which requires to save the action made --> save old sizeofdeck into an array that it may refer back to
                    sizeofdeck = olddeck[0]
                    print('cancel edit!')



                
        

            #initate Editing or quit editing
                    
            if event.key == pygame.K_ESCAPE:

                #are u sure u want to quit / save
                sizeofdeck = currentdecktext[9:]  #wrong command ?
                
                editdeckchange = False
                noteditingdeckchange = False
                clearselectdeckchange = False

                print('Return to gameMenu')

                
                gameMenu = 1
            if event.key == pygame.K_v:
                print('edit selection')
                card_viewer.main()  # Import the cardgame module
    

            if event.key == pygame.K_e:
                
                editdeckchange = True
                noteditingdeckchange = False
                clearselectdeckchange = False

                olddeck.append(sizeofdeck)
                
                print('edit selection')
    
            
                



    
    #read decks
    #read cards in deck
    #read card collection
    
    #currentdeck.read(1, len(currentdeck))

    #for i in currentdecktext.len():
        
    
    
    #create new deck in edit
    #newdeck.write()
    
    #move cards around
                
    #change decks, ask to save

    #calculate deck statss
                
    #only replace deck in save
    



    #gameBackground fill
    gameDisplay.fill(black)


    #mainmenu background
    changedeckbackground(0, 0)

    # Display a text menu on the top right
    message_to_screen2("Press ESC to return", newblue, 1400, 250)
    message_to_screen2("Press E to edit deck", newblue, 1400, 300)
    message_to_screen2("Press S to save deck", newblue, 1400, 350)
    message_to_screen2("Press C to clear deck", newblue, 1400, 400)
    message_to_screen2("Press Z to undo changes", newblue, 1400, 450)
    message_to_screen2("Press V to view all the cards", newblue, 1400, 500)



    #draw cards in the deck
    for i, d in enumerate(sizeofdeck):

        p = changedeckcardpos[i]
        drawCards(d,p)
        #print(d)


    #draw cards in the collection
    



    if(editdeckchange) == True:
        message_to_screen2("Editing Deck:", newblue, 1400, 500)

    if(noteditingdeckchange) == True:
        message_to_screen2("Saved Deck Edit!", newblue, 1400, 500)
        
    if(clearselectdeckchange) == True:
        message_to_screen2("Cleared Deck!", newblue, 1650, 500)
        
    

    #print(sizeofdeck)

    message_to_screen(sizeofdeck, red)
    #message_to_screen(currentdecktext, red)
    
    #message_to_screen(newdeck, red)


pass

global b_quit_button
b_quit_button = False

#########################
#   mainMenu function   #
#########################
def mainMenu():
    global gameMenu, b_quit_button
    #!event check
    for event in pygame.event.get():         
        
        # if statements to check for events:
        if event.type == pygame.QUIT:
            print('QUIT: by execution!')
            quitgame()
        elif event.type == pygame.KEYDOWN:      
            if event.key == pygame.K_q:
                #are u sure prompt then quit
                print('QUIT: by quit key!')
                if b_quit_button == True:
                    quitgame()
                b_quit_button = True
                

            if event.key == pygame.K_ESCAPE:
                #are u sure prompt then quit
                print('QUIT: by escape!')
                if b_quit_button == True:
                    quitgame()
                b_quit_button = True

            if event.key == pygame.K_c:
                print('cancel quit')
                b_quit_button = False
                
            if event.key == pygame.K_d:
                print('change deck selection!')
                gameMenu = 3

            if event.key == pygame.K_g:
                print('Enter game type selection!')
                gameMenu = 2

            if event.key == pygame.K_s:
                print('Enter setting selection!')
                gameMenu = 4

            if event.key == pygame.K_l:
                print('Enter learn game!')
                gameMenu = 0

    #gameBackground fill
    gameDisplay.fill(black)


    #mainmenu background
    drawImage(mainMenuBackgroundImg, 0, 0)

    message_title("Balanced Card Game", salmon)   
    
    pygame.draw.rect(gameDisplay, grey, (350, HEIGHT - 150, 80, 80))
    message_to_screen2("Player: _", pink, 450, HEIGHT - 150)
    message_to_screen2("Balance: \$0", green, 450, HEIGHT - 100)

    #mainmenu bar // # 1060, 20
    drawImage(mainmenubarImg,       860, 400)
    drawImage(playgamebuttonImg,    910, 380)
    drawImage(changedeckbuttonImg,  910, 520)
    drawImage(learnImg,  910, 660)
    drawImage(settingsbuttonImg,    910, 800)
    drawImage(logo_game_img,    WIDTH/1.4 - 200, 150)
    


    gameDisplay.blit(x_button_scaled,( WIDTH -300, 100))
    if b_quit_button == True:
        gameDisplay.blit(quitgamebutton_scaled,( WIDTH -400, 100))
        gameDisplay.blit(cancel_buttonImg,( WIDTH -800, 100))

    #display commands to select menu
    message_to_screen2("219 Studios", newblue, 100, 160)
    message_to_screen2("Version 0.3", newblue, 100, 200)
    message_to_screen2("Not Connected ...", newblue, 100, 260)
    if False:
        message_to_screen2("Connected", newblue, 100, 260)
    
pass          



def gametypeMenu():
    '''Game type selection menu function'''
    CURRENT_GAMEMODE_PAGE = 0
    global gameMenu
    #!event check
    for event in pygame.event.get():
                        #print(event)
        if event.type == pygame.QUIT:
            print('QUIT: by execution!')
            quitgame()
        elif event.type == pygame.KEYDOWN:                                                 
            if event.key == pygame.K_ESCAPE:
                print('Return to mainmenu!')
                gameMenu = 1
            if event.key == pygame.K_LEFT:
                print('Previous page')
                CURRENT_GAMEMODE_PAGE -= 1
                if CURRENT_GAMEMODE_PAGE < 0:
                    CURRENT_GAMEMODE_PAGE = 2

            if event.key == pygame.K_RIGHT:
                print('Next page')
                CURRENT_GAMEMODE_PAGE += 1
                if CURRENT_GAMEMODE_PAGE > 2:
                    CURRENT_GAMEMODE_PAGE = 0
            if event.key == pygame.K_h:
                print('Starting opening all gamemodes game types')
                import game_type
                game_type.main()
            if event.key == pygame.K_0:
                print('Starting 1 round game')
                import ladder_level1  # Import the game module
                ladder_level1.main()
            if event.key == pygame.K_1:
                print('Starting 1 round game')
                import game  # Import the game module
                game.main()
            if event.key == pygame.K_2:
                print('Starting full game')
                import rock_paper_scissors  # Import the game module
                rock_paper_scissors.main()  # Call the start_full_game function from game.py
            if event.key == pygame.K_3:
                print('Starting extended menu')
                import extended_game  # Import the game module
                extended_game.main()  # Call the start_full_game function from game.py
            if event.key == pygame.K_4:
                print('Starting online menu')
                import online_mode
                online_mode.main()  # Import the game module
                # onlineMenu()

    #gameBackground fill
    gameDisplay.fill(black)

    #mainmenu background
    drawImage(mainMenuBackgroundImg, 0, 0)
    drawImage(gobackbuttonImg,    100, 50)
    drawImage(gamemodesbuttonImg,    (WIDTH /2), 50)


    storymodeicon(80, 230)          # storymode
    oneroundicon(540, 230)          # one round mode
    traditionalroundicon(980, 230)  # traditional mode
    onlineroundicon (1440, 230)     # online mode


pass







##############################################################################################################################################
##############################################################################################################################################

##                                              MAIN SYSTEM FUNCTIONS                                                                       ##

##############################################################################################################################################
##############################################################################################################################################



#####################
#   Quit function   #
#####################
def quitgame():
    
    isRunning = False
    pygame.display.quit()
    pygame.quit()


pass

global b_learn_menu, num_learn_selection
b_learn_menu = False
num_learn_selection = 0

def learnMenu():
    '''Learn Game menu function'''
    global gameMenu
    global b_learn_menu
    global num_learn_selection

    help_lizared_spock = pygame.image.load('assets/help_lizard_spock.png').convert()
    help_classic = pygame.image.load('assets/help_classic.png').convert()
    help_extended = pygame.image.load('assets/help_extended.png').convert()

    #!event check
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('QUIT: by execution!')
            quitgame()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                print('Return to mainmenu!')
                gameMenu = 1
            if event.key == pygame.K_c:
                b_learn_menu = False
                num_learn_selection = 0
            if event.key == pygame.K_1:
                b_learn_menu = True
                num_learn_selection = 1
            if event.key == pygame.K_2:
                b_learn_menu = True
                num_learn_selection = 2
            if event.key == pygame.K_3:
                b_learn_menu = True
                num_learn_selection = 3

    #gameBackground fill
    gameDisplay.fill(black)

    # Display settings options
    message_title("Learn Game", red)

    if b_learn_menu == False:
        message_to_screen2("Press ESC to return to Main Menu", newblue, 100, 200)
        message_to_screen2("1. Rock, Paper Scissors", newblue, 100, 300)
        message_to_screen2("2. Lizard, Spock", newblue, 100, 350)
        message_to_screen2("3. Extended", newblue, 100, 400)
        message_to_screen2("4. Extended Plus", newblue, 100, 450)
        message_to_screen2("5. Tradiational Game", newblue, 100, 500)
        message_to_screen2("6. 1 Round Game", newblue, 100, 550)
        message_to_screen2("7. Auto CS Game", newblue, 100, 600)
        message_to_screen2("8. Captain's Mode Game", newblue, 100, 650)
    else:
        message_to_screen2("Press C to clear selection", newblue, 100, 250)
        if num_learn_selection == 1:
            message_to_screen2("1. Rock, Paper Scissors", newblue, 100, 200)
            gameDisplay.blit(help_classic, [300, 300])
        if num_learn_selection == 2:
            message_to_screen2("2. Lizard, Spock", newblue, 100, 200)
            gameDisplay.blit(help_lizared_spock, [300, 300])
        if num_learn_selection == 3:
            message_to_screen2("3. Extended", newblue, 100, 200)
            gameDisplay.blit(help_extended, [300, 300])

    

    pass

global b_toggle_game_setting
b_toggle_game_setting = False
def settingsMenu():
    '''Settings menu function'''
    global gameMenu, b_toggle_game_setting
    b_toggle_game_setting = False
    #!event check
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('QUIT: by execution!')
            quitgame()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                print('Return to mainmenu!')
                gameMenu = 1
            if event.key == pygame.K_g:
                print('toggle game setting')
                b_toggle_game_setting = not b_toggle_game_setting

    #gameBackground fill
    gameDisplay.fill(black)

    # Display settings options
    message_title("Settings Options", red)
    message_to_screen2("Press ESC to return to Main Menu", newblue, 100, 200)
    message_to_screen2("Volume: 0", newblue, 100, 500)
    message_to_screen2("< - Decrease volume", newblue, 100, 550)  # ▲ - &#9650; - \u25B2
    message_to_screen2("> - Increase volume", newblue, 100, 600)  # ▼ - &#9660; - \u25BC
    message_to_screen2("M - Mute Volume: True", newblue, 100, 650)
    message_to_screen2("F - Toggle Fullscreen: True", newblue, 100, 700)
    message_to_screen2("G - Game Setting: {b_toggle_game_setting}", newblue, 100, 750)

    
    
    pygame.draw.rect(gameDisplay, grey, (WIDTH - 700, 100, 80, 80))
    message_to_screen2("Player: _", pink, WIDTH - 600, 100)
    message_to_screen2("Balance: \$0", green, WIDTH - 600, 150)
    drawImage(logo_game_img,    WIDTH/1.5, HEIGHT - 550)
    # drawImage(logo_game_img_small,    WIDTH/1.6 -100, HEIGHT - 250 - 80)
    drawImage(logo_company_img_small,    WIDTH/1.6 -100, HEIGHT - 180 - 80)
    message_to_screen2("Balanced Card Game", salmon, WIDTH/1.6, HEIGHT - 300)
    message_to_screen2("219 Studios", white, WIDTH/1.6, HEIGHT - 250)
    message_to_screen2("www.219Studios.com/game/cardgame", teal, WIDTH/1.6, HEIGHT - 200)
    message_to_screen2("Game Version 0.2", grey, WIDTH/1.6, HEIGHT - 150)
    message_to_screen2("Python 3.10.11", grey, WIDTH/1.6, HEIGHT - 100)
    message_to_screen2("pygame 2.1.2 (SDL 2.0.18)", grey, WIDTH/1.6, HEIGHT - 50)
    pass

def onlineMenu():
    '''Online menu function'''
    global gameMenu
    #!event check
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('QUIT: by execution!')
            quitgame()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                print('Return to mainmenu!')
                gameMenu = 1

    #gameBackground fill
    gameDisplay.fill(black)

    # Display online options
    message_title("Online", red)
    message_to_screen2("Press ESC to return to Main Menu", newblue, 100, 200)
    message_to_screen2("Online Menu will go here.", newblue, 100, 300)
    pass



#####################
#   Main function   #
#####################
def main():
    '''Main function to run the game'''
    
    isRunning = True # boolean to run
    global gameMenu  # gameMenu
    gameMenu = 1
    
    try:
        while isRunning:
            #print(gameMenu)
            
            # 1 = mainmenu, 2 = gametype selection, 3 = change deck, 4 = settings, 5 = game1, 6 = game2, 7 = result page, 0
            #gameMenu check to switch gamemenu

            if gameMenu == 1:
                mainMenu()          # Main menu function
            elif gameMenu == 2:
                gametypeMenu()      # Game type selection function
            elif gameMenu == 3:
                changeDeckMenu()    # deck management function
            elif gameMenu == 4:
                settingsMenu()      # Settings menu function
            elif gameMenu == 0:     # learn game menu function
                learnMenu() 

                
            ##GAME 1##
            elif gameMenu == 5:
                break
            ##GAME 2##
            elif gameMenu == 6:
                gameLoop()
            ##CHECK FOR EXIT IF NOT RUNNING##
            if isRunning == False:
                break
            
            pygame.display.flip()   # Display Update function

            # display tickrate
            clock.tick(30)

    except SystemExit:
        message_to_screen("Quit game!", red) # quit message
        pygame.display.update()
        pygame.display.quit()
        pygame.quit()
    finally:
        currentdeckData.close()
        newdeck.close()

pass



#intial code
if __name__ == '__main__':    
    print('Ran successfully!')
    main()
